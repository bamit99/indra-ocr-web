"""Indra OCR web UI: upload PDF/images, get Markdown + JSON back."""
import io
import json
import os
import tempfile
import uuid

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, Response
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
    return """<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Indra OCR</title><style>
body{font-family:-apple-system,system-ui,sans-serif;max-width:640px;margin:48px auto;padding:0 16px;background:#0f1420;color:#e6e9ef}
h1{font-size:1.5rem} .card{background:#181f2e;border-radius:12px;padding:24px;box-shadow:0 4px 16px rgba(0,0,0,.4)}
input,select{margin:8px 0;font-size:1rem} input[type=file]{width:100%} select{padding:6px}
button{background:#4f7cf7;color:#fff;border:0;border-radius:8px;padding:10px 22px;font-size:1rem;cursor:pointer;margin-top:8px}
button:disabled{opacity:.5} #status{margin-top:12px;color:#9fb0c8} a{color:#7ea4ff}
</style></head><body><div class=card>
<h1>🔍 Indra OCR</h1><p>Upload a PDF or image → get Markdown and JSON.</p>
<form id=f><input type=file name=file accept=".pdf,.png,.jpg,.jpeg,.webp,.bmp,.tif,.tiff" required>
<br><label><input type=checkbox name=math> Math as LaTeX (slower)</label><br>
<button id=go>Convert</button><div id=status></div></form>
<div id=result style=display:none><hr><div>Download: <a id=dlmd href=#>Markdown (.md)</a> · <a id=dljson href=#>JSON (.jsonl)</a></div><div style=margin-top:6px><b>Markdown preview:</b></div><pre id=out style="white-space:pre-wrap;max-height:50vh;overflow:auto;background:#0b101c;padding:12px;border-radius:8px;font-size:.85rem"></pre><div style=margin-top:6px><b>JSON (first page):</b></div><pre id=outj style="white-space:pre-wrap;max-height:30vh;overflow:auto;background:#0b101c;padding:12px;border-radius:8px;font-size:.8rem"></pre></div></div>
<script>
f.onsubmit=async e=>{e.preventDefault();const s=document.getElementById('status');s.textContent='Working… (first run downloads ~18MB models)';document.getElementById('go').disabled=true;document.getElementById('result').style.display='none';
try{const r=await fetch('/convert',{method:'POST',body:new FormData(f)});if(!r.ok){s.textContent='Error '+(await r.text());return}
const j=await r.json();const o=document.getElementById('out');o.textContent=j.md.length>20000?j.md.slice(0,20000)+'\\n…(truncated preview; use download)':j.md;
const oj=document.getElementById('outj');const jl=j.json.split('\\n');oj.textContent=jl.length>40?jl.slice(0,40).join('\\n')+'\\n…(truncated; use download)':j.json;
document.getElementById('dlmd').href='/download/'+j.id+'?fmt=md';document.getElementById('dljson').href='/download/'+j.id+'?fmt=json';s.textContent='Done: '+j.pages+' page(s) in '+j.seconds+'s';document.getElementById('result').style.display='block'}
catch(err){s.textContent='Error: '+err}finally{document.getElementById('go').disabled=false}};
</script></body></html>"""


@app.post("/convert")
async def convert(file: UploadFile = File(...), math: bool = Form(False)):
    rid = uuid.uuid4().hex[:12]
    name = os.path.basename(file.filename or "input.pdf")
    ext = os.path.splitext(name)[1].lower()
    path = os.path.join(TMP, rid + ext)
    with open(path, "wb") as f:
        f.write(await file.read())
    conv = indra_ocr.load(threads=2, math=math)
    import time
    t0 = time.time()
    pages = list(conv.convert(path, max_pages=200))
    secs = round(time.time() - t0, 1)
    md, jsonl, n_pages = _render(iter(pages), name)
    RESULTS[rid] = {"name": name, "md": md, "json": jsonl}
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