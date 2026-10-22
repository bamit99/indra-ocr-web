# 🔍 Indra OCR Web

A tiny self-hosted web UI around [Indra OCR](https://huggingface.co/datalab-to/indra-ocr) — upload a PDF or image in your browser, get back **Markdown** and **JSON** (lines, bounding boxes, layout blocks, confidences) for download.

Built for anyone who wants OCR-as-a-service on their own machine with zero GPU: Indra OCR is a ~1.25M-parameter recogniser (~7.3M parameters across all default models), ~76MB of ONNX models, and runs fast on plain CPUs.

## Features

- 📄 Upload **PDF or images** (PNG, JPG, WEBP, BMP, TIFF)
- 📝 **Markdown** output preserving document structure (headings, lists, tables as HTML)
- 🧾 **JSON output** per page: `source`, `markdown`, `text`, layout `blocks` (with labels like Section-Header, Table, Caption), `lines` with bounding boxes and confidences
- 🧮 Optional **math mode** — output inline LaTeX
- 🖥️ Inline previews of both Markdown and JSON before downloading
- 🐳 Single-container Docker deployment, models cached in a volume, no PyTorch

## Requirements

- [Docker](https://docs.docker.com/get-docker/) with Docker Compose (tested with Docker 29.x / Compose v2)
- ~2GB RAM available for the container (CPU only — no GPU needed)
- Internet access on first start to download the ~76MB of models from Hugging Face (cached afterwards)
- Python **3.10+** only if you want to run without Docker

## Quickstart (Docker — recommended)

```sh
git clone https://github.com/bamit99/indra-ocr-web.git
cd indra-ocr-web
docker compose up -d --build
```

Then open **http://localhost:8310** in your browser, drop in a PDF or image, and grab the Markdown / JSON downloads.

To run it during the day only or manage lifecycle:

```sh
docker compose down      # stop
docker compose logs -f   # follow logs
```

### Run without Docker

```sh
python3 -m venv .venv && source .venv/bin/activate   # Python 3.10+
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8310
```

## API

The UI is plain HTML, but the backend is a small FastAPI app you can drive programmatically:

```sh
# Convert (returns JSON with id, md and json fields)
curl -F "file=@document.pdf" http://localhost:8310/convert

# Download results for a previous conversion
curl -o out.md        "http://localhost:8310/download/<id>?fmt=md"
curl -o out.jsonl     "http://localhost:8310/download/<id>?fmt=json"
```

`POST /convert` accepts: `file` (PDF/image, required), `math` (`true`/`false`, optional — LaTeX math output).
`GET /download/{id}?fmt=md|json` returns the corresponding artifact.

## Configuration

- `HF_HOME=/data/hf` env var — where models are cached (mounted as the `indra-models` volume in the provided compose file)
- Concurrency is fixed at 2 OCR threads per conversion inside the app (see `indra_ocr.load(threads=2)` in `app.py`)
- Page limit per document: 200 (adjust `max_pages` in `app.py`)

## Acknowledgements & Licenses

- Powered by [Indra OCR](https://huggingface.co/datalab-to/indra-ocr) by [Datalab](https://www.datalab.to/) — this wrapper's code is MIT-licensed, **but** the Indra OCR model weights use a modified [OpenRAIL-M](https://huggingface.co/datalab-to/indra-ocr/blob/main/LICENSE) license: free for research, personal use, and startups under $20M funding/revenue; not for use competitively with Datalab's API. Commercial usage beyond that requires a license from Datalab.
- Thanks to ONNX Runtime, pypdfium2, OpenCV, and FastAPI.

## Known limitations (inherited from Indra OCR)

- Clean printed documents work best; handwriting and degraded scans read poorly
- Complex tables (merged/spanning cells) can come out scrambled
- OCR on images covers Latin (~50 languages), Cyrillic, Greek, Devanagari, Bengali, Chinese; other scripts work only via a digital PDF's text layer