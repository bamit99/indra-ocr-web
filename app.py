"""Indra OCR web UI: upload PDF/images, get Markdown + JSON back."""
import io
import json
import os
import tempfile
import uuid

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
import indra_ocr

app = FastAPI(title="Indra OCR Web", docs_url=None, redoc_url=None)

TMP = tempfile.mkdtemp(prefix="indra-")
RESULTS = {}  # id -> {filename, fmt, pages: [(source, markdown/text/json)]}


def _render(conv, fname):
    md_parts, json_parts = [], []
    n_pages = 0
    for i, page in conv:
        n_pages += 1
        src = getattr(page, "source", "")
        d = {"file": fname, "page": i, "source": src}
        for attr in ("markdown", "text"):
            v = getattr(page, attr, None)
            if v is not None:
                d[attr] = v
        blocks = getattr(page, "blocks", None)
        if blocks is not None:
            d["blocks"] = blocks
        lines = getattr(page, "lines", None)
        if lines is not None:
            d["lines"] = [
                {"text": getattr(l, "text", None),
                 "box": getattr(getattr(l, "box", None), "__iter__", None) and list(l.box),
                 "conf": getattr(l, "conf", None)} for l in lines
            ]
        json_parts.append(json.dumps(d, ensure_ascii=False))
        if md_parts:
            md_parts.append("\n\n---\n\n")
        md_parts.append(getattr(page, "markdown", "") or getattr(page, "text", ""))
    md = "\n\n".join(str(p) for p in md_parts) if md_parts else ""
    return md, "\n".join(json_parts), n_pages


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Indra OCR — Intake Desk</title>
<style>
@font-face{font-family:'Libre Caslon Display';src:url('/static/fonts/LibreCaslonDisplay-Regular.ttf') format('truetype');font-weight:400;font-display:swap}
@font-face{font-family:'Archivo';src:url('/static/fonts/Archivo.ttf') format('truetype');font-weight:100 900;font-display:swap}
@font-face{font-family:'Courier Prime';src:url('/static/fonts/CourierPrime-Regular.ttf') format('truetype');font-weight:400;font-display:swap}
@font-face{font-family:'Courier Prime';src:url('/static/fonts/CourierPrime-Bold.ttf') format('truetype');font-weight:700;font-display:swap}
:root{
  --paper:#F4EFE4; --panel:#FBF8F1; --ink:#1A1712; --ink-soft:#554C3F; --ink-faint:#6B6152;
  --rule:#C9BFA9; --rule-soft:#E2D9C6;
  --vermilion:#C8371E; --vermilion-deep:#A82C16; --vermilion-wash:#F6E4DC;
  --mono:'Courier Prime',ui-monospace,'Courier New',monospace;
  --sans:'Archivo',system-ui,sans-serif;
  --display:'Libre Caslon Display',Georgia,serif;
}
*{box-sizing:border-box}
html{caret-color:var(--vermilion)}
body{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.55 var(--sans);
  -webkit-font-smoothing:antialiased}
::selection{background:var(--vermilion-wash);color:var(--ink)}
a{color:var(--vermilion);text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{color:var(--vermilion-deep)}
:focus-visible{outline:2px solid var(--vermilion);outline-offset:2px}
.wrap{max-width:760px;margin:0 auto;padding:0 20px}

/* masthead */
header{border-bottom:1px solid var(--rule);background:var(--paper);position:relative}
header::after{content:"";position:absolute;left:0;right:0;bottom:3px;height:1px;background:var(--rule)}
.masthead{display:flex;align-items:baseline;gap:14px;padding:34px 0 10px}
.mark{flex:0 0 auto;align-self:center;color:var(--vermilion)}
h1{margin:0;font:400 clamp(30px,6vw,44px)/1.05 var(--display);letter-spacing:.01em}
.shelf{margin-left:auto;font:400 11px/1.4 var(--mono);letter-spacing:.14em;color:var(--ink-faint);
  text-transform:uppercase;white-space:nowrap}
.meta-rule{padding:0 0 12px;font:600 11px/1.6 var(--sans);letter-spacing:.22em;
  text-transform:uppercase;color:var(--ink-soft)}

/* accession panel */
main{padding:30px 0 8px}
.panel{background:var(--panel);border:1px solid var(--rule);padding:26px 26px 22px}
.panel h2{margin:0 0 18px;font:600 12px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;
  color:var(--ink-soft);display:flex;align-items:center;gap:10px}
.panel h2::after{content:"";flex:1;height:1px;background:var(--rule-soft)}
.field{margin:0 0 16px}
.field-label{display:block;font:600 11px/1 var(--sans);letter-spacing:.18em;
  text-transform:uppercase;color:var(--ink-soft);margin-bottom:7px}
.drop{border:1px dashed var(--rule);background:#fff;padding:20px;text-align:center;
  cursor:pointer;position:relative;transition:border-color .18s,background .18s}
.drop:hover{border-color:var(--ink-soft)}
.drop.over{border-color:var(--vermilion);background:var(--vermilion-wash)}
.drop:focus-within{outline:2px solid var(--vermilion);outline-offset:2px}
.drop input[type=file]{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
#docname{font:400 15px/1.4 var(--mono);color:var(--ink);word-break:break-all}
#docname.empty{color:var(--ink-faint)}
.hint{margin-top:6px;font:400 12px/1.5 var(--sans);color:var(--ink-faint)}
.checkrow{display:flex;align-items:center;gap:9px;padding:2px 0 20px}
.checkrow input{accent-color:var(--vermilion);width:16px;height:16px}
.checkrow label{font:400 14.5px/1.4 var(--sans)}
.checkrow .slow{font:400 12px var(--mono);color:var(--ink-faint)}
button{font:600 12.5px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;
  background:var(--vermilion);color:#fff;border:0;border-radius:2px;padding:14px 30px;
  cursor:pointer;transition:background .15s,transform .05s}
button:hover{background:var(--vermilion-deep)}
button:active{transform:translateY(1px)}
button:disabled{background:var(--ink-faint);cursor:not-allowed;transform:none}

/* ledger + stamps */
.ledger{display:flex;align-items:center;gap:14px;margin-top:18px;border-top:1px solid var(--rule-soft);
  padding-top:14px;min-height:38px;flex-wrap:wrap}
.stamp{font:700 11px/1 var(--mono);letter-spacing:.22em;text-transform:uppercase;
  border:2px solid currentColor;border-radius:3px;padding:6px 10px 5px;transform:rotate(-2.5deg)}
.stamp.accessioned{color:var(--ink)}
.stamp.processing{color:var(--ink-soft)}
.stamp.digitized{color:var(--vermilion);animation:press .5s cubic-bezier(.2,.9,.3,1.2) both}
.stamp.err{color:var(--vermilion);animation:press .5s cubic-bezier(.2,.9,.3,1.2) both}
@keyframes press{from{transform:rotate(-8deg) scale(1.7);opacity:0}to{transform:rotate(-2.5deg) scale(1);opacity:1}}
#ledgertext{font:400 13px/1.5 var(--mono);color:var(--ink-soft);font-variant-numeric:tabular-nums}

/* results */
#result{margin-top:30px}
#result[hidden]{display:none}
.stubs{display:flex;gap:14px;flex-wrap:wrap}
.stub{flex:1 1 200px;border:1px solid var(--rule);background:var(--panel);padding:14px 16px;
  display:flex;flex-direction:column;gap:4px}
.stub .kind{font:600 11px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--ink-soft)}
.stub a{font:700 14px/1.4 var(--mono);color:var(--vermilion);word-break:break-all}
.stub .desc{font:400 12px/1.45 var(--sans);color:var(--ink-faint)}
.previews{display:flex;gap:14px;margin-top:14px;flex-wrap:wrap}
.preview{flex:1 1 300px;margin:0;border:1px solid var(--rule);background:#fff}
.preview figcaption{font:600 11px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;
  color:var(--ink-soft);padding:10px 14px;border-bottom:1px solid var(--rule-soft)}
.preview pre{margin:0;padding:14px;max-height:44vh;overflow:auto;white-space:pre-wrap;
  word-break:break-word;font:400 13px/1.6 var(--mono);color:var(--ink)}
.preview.json pre{font-size:12px}
.empty-note{font:400 13px var(--sans);color:var(--ink-faint)}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-track{background:var(--paper)}
::-webkit-scrollbar-thumb{background:var(--rule);border:2px solid var(--paper);border-radius:5px}
::-webkit-scrollbar-thumb:hover{background:var(--ink-faint)}
html{scrollbar-color:var(--rule) var(--paper);scrollbar-width:thin}

/* footer */
footer{border-top:1px solid var(--rule);margin-top:44px;padding:18px 0 34px;position:relative}
footer::before{content:"";position:absolute;left:0;right:0;top:3px;height:1px;background:var(--rule)}
.foot-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;
  font:600 11px/1.7 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft)}
.foot-row .callno{font:400 11px var(--mono);letter-spacing:.1em;color:var(--ink-faint)}
.foot-row .right{margin-left:auto}
.foot-row a{color:var(--vermilion)}
.copyright-name{color:var(--ink)}

@media (max-width:560px){
  .masthead{flex-wrap:wrap;padding-top:24px}
  .shelf{margin-left:0;width:100%}
  .panel{padding:20px 16px}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.001s!important;transition-duration:.001s!important}
}
</style>
</head>
<body>
<header><div class="wrap">
  <div class="masthead">
    <svg class="mark" width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="11" cy="11" r="6.2" fill="none" stroke="currentColor" stroke-width="1.6"/><line x1="11" y1="0" x2="11" y2="22" stroke="currentColor" stroke-width="1.6"/><line x1="0" y1="11" x2="22" y2="11" stroke="currentColor" stroke-width="1.6"/></svg>
    <h1>Indra OCR</h1>
    <span class="shelf">MS·INDRA·2026</span>
  </div>
  <div class="meta-rule">Self-hosted · CPU-only</div>
</div></header>

<main><div class="wrap">
  <section class="panel" aria-labelledby="intake-h">
    <h2 id="intake-h">Accession intake</h2>
    <form id="f">
      <div class="field">
        <span class="field-label" id="doclabel">Document</span>
        <div class="drop" id="drop">
          <input type="file" id="file" name="file" accept=".pdf,.png,.jpg,.jpeg,.webp,.bmp,.tif,.tiff" required aria-labelledby="doclabel">
          <span id="docname" class="empty">Drop a PDF or image here, or click to choose</span>
          <div class="hint">PDF, PNG, JPG, WEBP, BMP, TIFF · up to 200 pages</div>
        </div>
      </div>
      <div class="checkrow">
        <input type="checkbox" id="math" name="math">
        <label for="math">Math mode: equations as LaTeX <span class="slow">(slower)</span></label>
      </div>
      <button id="go" type="submit">Begin conversion</button>
    </form>
    <div class="ledger" role="status" aria-live="polite">
      <span class="stamp accessioned" id="stamp" hidden>Accessioned</span>
      <span id="ledgertext">Desk ready, awaiting document.</span>
    </div>
  </section>

  <section id="result" hidden aria-label="Results">
    <div class="stubs">
      <div class="stub"><span class="kind">Claim stub — one</span><a id="dlmd" href="#">Markdown (.md)</a><span class="desc">Structured text: headings, lists, tables.</span></div>
      <div class="stub"><span class="kind">Claim stub — two</span><a id="dljson" href="#">JSONL (.jsonl)</a><span class="desc">Lines, bounding boxes, layout blocks, confidences.</span></div>
    </div>
    <div class="previews">
      <figure class="preview"><figcaption>Reading copy: Markdown</figcaption><pre id="out"></pre></figure>
      <figure class="preview json"><figcaption>Record copy: JSON</figcaption><pre id="outj"></pre></figure>
    </div>
  </section>
</div></main>

<footer><div class="wrap"><div class="foot-row">
  <span class="callno">Collection MS·INDRA·2026</span>
  <span class="right">© 2026 <span class="copyright-name">Amit Bhatnagar</span> · <a href="https://github.com/bamit99">github.com/bamit99</a></span>
</div></div></footer>

<script>
var f=document.getElementById('f'),go=document.getElementById('go'),drop=document.getElementById('drop'),
    fileInput=document.getElementById('file'),docname=document.getElementById('docname'),
    stamp=document.getElementById('stamp'),ledgertext=document.getElementById('ledgertext'),
    result=document.getElementById('result'),timer=null;

function setStamp(text,cls){stamp.hidden=false;stamp.textContent=text;stamp.className='stamp '+cls;
  void stamp.offsetWidth;}
function fmt(ms){var s=ms/1000,m=Math.floor(s/60);s=(s-m*60);return (m<10?'0':'')+m+':'+(s<10?'0':'')+s.toFixed(1);}
function showName(){var n=fileInput.files.length?fileInput.files[0].name:'';
  docname.textContent=n||'Drop a PDF or image here, or click to choose';
  docname.className=n?'':'empty';}

drop.addEventListener('click',function(){fileInput.click();});
fileInput.addEventListener('change',showName);
['dragenter','dragover'].forEach(function(ev){drop.addEventListener(ev,function(e){
  e.preventDefault();drop.classList.add('over');});});
['dragleave','drop'].forEach(function(ea){drop.addEventListener(ea,function(e){
  e.preventDefault();drop.classList.remove('over');});});
drop.addEventListener('drop',function(e){if(e.dataTransfer.files.length){
  fileInput.files=e.dataTransfer.files;showName();}});

f.onsubmit=async function(e){e.preventDefault();
  if(go.disabled)return;
  go.disabled=true;go.textContent='Processing…';result.hidden=true;
  setStamp('Accessioned','accessioned');
  var t0=Date.now();
  ledgertext.textContent='Accessioned: '+fileInput.files[0].name;
  timer=setInterval(function(){
    if(stamp.textContent!=='Processing'){setStamp('Processing','processing');}
    ledgertext.textContent='Processing, elapsed '+fmt(Date.now()-t0)+
      '. First accession downloads ~18 MB models (one time).';},100);
  try{
    var r=await fetch('/convert',{method:'POST',body:new FormData(f)});
    if(!r.ok){throw new Error('server replied '+r.status+' — '+(await r.text()).slice(0,200));}
    var j=await r.json();
    var o=document.getElementById('out');
    o.textContent=j.md.length>20000?j.md.slice(0,20000)+'\\n…(truncated preview; download for full text)':j.md;
    if(!j.md.trim()){o.innerHTML='<span class="empty-note">No text recognised. Try a higher-contrast scan.</span>';}
    var oj=document.getElementById('outj'),jl=j.json.split('\\n');
    oj.textContent=jl.length>40?jl.slice(0,40).join('\\n')+'\\n…(truncated; download for full record)':jl.slice(0,40).join('\\n');
    document.getElementById('dlmd').href='/download/'+j.id+'?fmt=md';
    document.getElementById('dljson').href='/download/'+j.id+'?fmt=json';
    clearInterval(timer);
    setStamp('Digitized','digitized');
    ledgertext.textContent='Call number INDRA·'+j.id+', '+j.pages+' page(s) in '+j.seconds+'s. Claim stubs below.';
    result.hidden=false;
  }catch(err){
    clearInterval(timer);
    setStamp('Error','err');
    ledgertext.textContent='Conversion failed: '+err.message+'. Check the file type and retry.';
  }finally{go.disabled=false;go.textContent='Begin conversion';}
};
</script>
</body>
</html>"""


@app.post("/convert")
async def convert(file: UploadFile = File(...), math: bool = Form(False)):
    rid = uuid.uuid4().hex[:12]
    name = os.path.basename(file.filename or "input.pdf")
    ext = os.path.splitext(name)[1].lower()
    path = os.path.join(TMP, rid + ext)
    with open(path, "wb") as f:
        f.write(await file.read())
    try:
        conv = indra_ocr.load(threads=2, math=math)
        import time
        t0 = time.time()
        pages = list(conv.convert(path, max_pages=200))
        secs = round(time.time() - t0, 1)
        md, jsonl, n_pages = _render(iter(pages), name)
        RESULTS[rid] = {"name": name, "md": md, "json": jsonl}
    finally:
        os.remove(path)
    return {"id": rid, "pages": n_pages, "seconds": secs,
            "md": md, "json": jsonl}


@app.get("/download/{rid}")
def download(rid: str, fmt: str = "md"):
    r = RESULTS.get(rid)
    if not r:
        return Response("Not found (server restarted?)", status_code=404)
    base = os.path.splitext(r["name"])[0]
    if fmt == "json":
        out, ext = r["json"], ".jsonl"
    else:
        out, ext = r["md"], ".md"
    fname = base + ext
    media = "application/json; charset=utf-8" if ext == ".jsonl" else "text/plain; charset=utf-8"
    return Response(out, media_type=media,
                    headers={"Content-Disposition": f"attachment; filename={fname}"})


app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")), name="static")