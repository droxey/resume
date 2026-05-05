#!/usr/bin/env python3
"""
Rebuild the AI Technologist resume package.

Usage:
    python build_resume_assets.py

Source of truth:
    2026-05-05_Resume_AI_Technologist_ATS.md

Outputs:
    2026-05-05_Resume_AI_Technologist_ATS.html
    2026-05-05_Resume_AI_Technologist_ATS.pdf
    2026-05-05_Resume_AI_Technologist_ATS_assets.zip

The script also validates LINKEDIN.md and README.md, then includes them in the ZIP.
"""

from __future__ import annotations

from pathlib import Path
import html
import re
import zipfile

import fitz
from weasyprint import HTML

BASE = "2026-05-05_Resume_AI_Technologist_ATS"
ROOT = Path(__file__).resolve().parent
MD = ROOT / f"{BASE}.md"
HTML_FILE = ROOT / f"{BASE}.html"
PDF = ROOT / f"{BASE}.pdf"
ZIP = ROOT / f"{BASE}_assets.zip"
LINKEDIN = ROOT / "LINKEDIN.md"
README = ROOT / "README.md"

CSS = r"""
  :root { --ink:#141414; --muted:#444; --rule:#c9c9c9; --link:#0645ad; }
  @page { size: Letter; margin: 0.44in 0.47in 0.44in 0.47in; }
  * { box-sizing: border-box; }
  html, body { margin:0; padding:0; }
  body { font-family: Arial, Helvetica, sans-serif; color:var(--ink); background:#fff; font-size:8.65pt; line-height:1.18; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  main { max-width:8.05in; margin:0 auto; padding:0; }
  h1 { font-size:19.5pt; line-height:1; margin:0 0 5px 0; letter-spacing:-0.25px; }
  h2 { font-size:10.9pt; line-height:1.05; margin:13px 0 6px 0; padding:0 0 2px 0; text-transform:uppercase; letter-spacing:0.45px; border-bottom:1px solid var(--rule); }
  h3 { font-size:9.7pt; line-height:1.1; margin:10px 0 3px 0; }
  p { margin:0 0 5.4px 0; }
  .title { margin-bottom:3px; }
  .contact { margin:0 0 2.2px 0; display:block; }
  .resume-header { text-align:center; margin:0 0 5px 0; }
  .resume-header h1 { text-align:center; }
  .resume-header .title, .resume-header .contact { text-align:center; }
  ul { margin:0 0 7px 13px; padding:0; }
  li { margin:0 0 2.65px 0; padding-left:1px; }
  a { color:var(--link); text-decoration:underline; }
  strong { font-weight:700; }
  code { font-family:Arial, Helvetica, sans-serif; }
  hr { border:0; margin:5px 0; }
  h2, h3 { break-after:avoid; page-break-after:avoid; }
  li, p { break-inside:avoid; page-break-inside:avoid; }
  .page-start { break-before:page; page-break-before:always; margin-top:0; }
  .job { break-inside:avoid; page-break-inside:avoid; }
  @media screen { body{background:#f3f3f3;} main{background:#fff; padding:0.44in 0.47in; min-height:11in; box-shadow:0 0 0 1px #ddd;} }
"""


def inline_md(text: str) -> str:
    """Tiny inline Markdown renderer for this resume."""
    text = html.escape(text, quote=True)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', text)
    # Run twice so bold can wrap links already converted to HTML.
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def close_list(out: list[str], in_list: bool) -> bool:
    if in_list:
        out.append("</ul>")
    return False


def close_job(out: list[str], in_job: bool) -> bool:
    if in_job:
        out.append("</section>")
    return False


def build_html_from_markdown() -> None:
    md = MD.read_text(encoding="utf-8")
    lines = md.splitlines()
    out: list[str] = []
    in_header = False
    header_done = False
    in_list = False
    in_job = False
    current_h2 = ""

    out.append("<!DOCTYPE html>")
    out.append('<html lang="en">')
    out.append("<head>")
    out.append('<meta charset="utf-8"/>')
    out.append('<meta name="viewport" content="width=device-width, initial-scale=1"/>')
    out.append("<title>Dani Roxberry - AI Technologist Resume</title>")
    out.append("<style>" + CSS + "</style>")
    out.append("</head>")
    out.append("<body>")
    out.append("<main>")

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        if line.startswith('<div align="center">') or line.startswith("<div align='center'>"):
            in_header = True
            out.append('<div class="resume-header">')
            continue
        if line == "</div>":
            in_header = False
            header_done = True
            out.append("</div>")
            continue

        if line == "---":
            in_list = close_list(out, in_list)
            if current_h2 not in {"Professional Experience", "Earlier Experience"}:
                in_job = close_job(out, in_job)
            out.append("<hr/>")
            continue

        if line.startswith("# "):
            in_list = close_list(out, in_list)
            if in_header:
                out.append(f"<h1>{inline_md(line[2:].strip())}</h1>")
            else:
                out.append(f"<h1>{inline_md(line[2:].strip())}</h1>")
            continue

        if line.startswith("## "):
            in_list = close_list(out, in_list)
            in_job = close_job(out, in_job)
            current_h2 = line[3:].strip()
            cls = ""
            if current_h2 == "Selected Applied AI Projects":
                cls = ' class="page-start selected-projects"'
            out.append(f"<h2{cls}>{inline_md(current_h2)}</h2>")
            continue

        if line.startswith("### "):
            in_list = close_list(out, in_list)
            heading = line[4:].strip()
            if current_h2 in {"Professional Experience", "Earlier Experience"}:
                in_job = close_job(out, in_job)
                cls = ' class="job page-start"' if heading.startswith("FrameBuzz -") else ' class="job compact-job"' if current_h2 == "Earlier Experience" else ' class="job"'
                out.append(f"<section{cls}>")
                in_job = True
            out.append(f"<h3>{inline_md(heading)}</h3>")
            continue

        if line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_md(line[2:].strip())}</li>")
            continue

        in_list = close_list(out, in_list)
        cls = ""
        if in_header:
            if line.startswith("**") and line.endswith("**"):
                cls = ' class="title"'
            else:
                cls = ' class="contact"'
        out.append(f"<p{cls}>{inline_md(line)}</p>")

    in_list = close_list(out, in_list)
    in_job = close_job(out, in_job)
    out.append("</main>")
    out.append("</body>")
    out.append("</html>")
    HTML_FILE.write_text("\n".join(out), encoding="utf-8")


def build_pdf() -> None:
    HTML(filename=str(HTML_FILE), base_url=str(ROOT)).write_pdf(str(PDF))


def markdown_links() -> list[str]:
    text = MD.read_text(encoding="utf-8")
    return re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", text)


def pdf_links() -> list[str]:
    doc = fitz.open(PDF)
    links: list[str] = []
    for page in doc:
        for link in page.get_links():
            uri = link.get("uri")
            if uri:
                links.append(uri)
    return links


def page_texts() -> list[str]:
    doc = fitz.open(PDF)
    return [page.get_text() for page in doc]


def verify_toc(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "## Table of Contents" not in text:
        raise RuntimeError(f"{path.name} must include a Table of Contents.")


def verify() -> None:
    if not LINKEDIN.exists():
        raise RuntimeError("LINKEDIN.md is missing.")
    if not README.exists():
        raise RuntimeError("README.md is missing.")
    verify_toc(LINKEDIN)
    verify_toc(README)

    doc = fitz.open(PDF)
    pages = page_texts()
    full_text = "\n".join(pages)
    if doc.page_count != 3:
        raise RuntimeError(f"Expected 3 PDF pages, got {doc.page_count}.")
    if "Open to San Francisco" in full_text:
        raise RuntimeError("Removed hybrid/travel phrase leaked back into PDF.")
    if "Dani Roxberry" not in full_text or "AI Technologist" not in full_text:
        raise RuntimeError("Generated PDF appears to be missing resume header text.")
    if "SELECTED APPLIED AI PROJECTS" not in pages[1]:
        raise RuntimeError("Selected Applied AI Projects must start on page 2.")
    if "FrameBuzz - Founder / Inventor / Chief Technology Officer" not in pages[2]:
        raise RuntimeError("FrameBuzz must start on page 3.")
    md_urls = sorted(set(markdown_links()))
    pdf_urls = sorted(set(pdf_links()))
    if md_urls != pdf_urls:
        raise RuntimeError(f"Markdown/PDF link mismatch. MD={md_urls} PDF={pdf_urls}")


def build_zip() -> None:
    files = [MD, HTML_FILE, PDF, LINKEDIN, Path(__file__).resolve(), README]
    with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in files:
            z.write(path, path.name)


def main() -> None:
    build_html_from_markdown()
    build_pdf()
    verify()
    build_zip()
    print(f"Built {ZIP}")


if __name__ == "__main__":
    main()
