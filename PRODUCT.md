# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Self-hosters, developers, researchers who want OCR on their own machine without a GPU. Situation: at their own laptop/server, converting scanned PDFs or images to usable text. Job: upload document, get Markdown + structured JSON, download both. (Inferred from README; not separately confirmed by user.)

## Product Purpose

Tiny self-hosted web UI around Indra OCR: upload PDF/image, get Markdown and JSON (lines, bounding boxes, layout blocks, confidences) back. Success = conversion done and files downloaded, on plain CPU, ~18MB ONNX model, zero GPU.

## Positioning

OCR-as-a-service on your own machine: ~1M-parameter ONNX model, single Docker container, no PyTorch, no cloud upload of documents.

## Operating Context

- Browser page at localhost:8310; backend drivable via `POST /convert`, `GET /download/{id}`
- First run downloads ~18MB models from Hugging Face (cached in volume)
- CPU-only, ~2GB RAM container

## Capabilities and Constraints

- Upload PDF or images (PNG, JPG, WEBP, BMP, TIFF), max 200 pages
- Optional math mode (LaTeX output, slower)
- Markdown preview + JSON preview inline; download .md and .jsonl
- Single-page UI embedded as inline HTML string in `app.py`; FastAPI backend must keep working unchanged
- Footer must credit: Copyright © 2026 Amit Bhatnagar + GitHub link (github.com/bamit99)
- Full visual overhaul approved; features and API stay untouched

## Evidence on Hand

- README.md documents all features, API, limits
- Working backend in app.py (conversion, downloads)
- No logos, brand assets, or screenshots on hand. No testimonials/customers/pricing — must not be fabricated.

## Product Principles

1. Zero-friction: page loads, drop file, convert, download
2. Honest about limits (handwriting, complex tables, script coverage)
3. Self-hosted privacy: documents never leave the machine
4. Light footprint: CPU-only, small model, single container

