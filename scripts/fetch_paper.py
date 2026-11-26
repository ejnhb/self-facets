"""Download an arXiv paper and make its figures visible for coding.

Text tools (alphaXiv page content, web fetchers) return figure captions but not the figures. This script gets the
PDF, writes its text with page markers, finds the pages that hold figures (captions starting "Figure N" or
"Fig. N", and pages with embedded images), and renders those pages to PNG so a coder can look at them.

    python3 scripts/fetch_paper.py 2611.15267v2            # into _paper/2611.15267v2/
    python3 scripts/fetch_paper.py 2611.15267v2 --all      # render every page
    python3 scripts/fetch_paper.py 2611.15267v2 --dpi 150

Needs curl and poppler-utils (pdftotext, pdftoppm, pdfimages). `_paper/` is git-ignored: downloads stay local.
Say in the record's `read_parts` which figure pages you looked at (the script prints them).
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPTION = re.compile(r"^\s*(Figure|Fig\.)\s*(\d+)\s*[:.|]", re.MULTILINE)


def run(*cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arxiv_id", help="arXiv id with version, e.g. 2611.15267v2 (the version you will code)")
    ap.add_argument("--out", default=None, help="output directory (default _paper/<id>)")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--all", action="store_true", help="render every page, not only figure pages")
    a = ap.parse_args()

    if not re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", a.arxiv_id):
        sys.exit("arxiv_id should look like 2611.15267v2")
    if not re.search(r"v\d+$", a.arxiv_id):
        print("note: no version given; arXiv serves the latest, which may not be the version you code", file=sys.stderr)
    out = Path(a.out) if a.out else ROOT / "_paper" / a.arxiv_id
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / f"{a.arxiv_id}.pdf"
    if not pdf.exists():
        run("curl", "-sSfL", "-o", str(pdf), f"https://arxiv.org/pdf/{a.arxiv_id}")
    if pdf.read_bytes()[:4] != b"%PDF":
        sys.exit(f"{pdf} is not a PDF; the download may have been refused")

    pages = int(re.search(r"Pages:\s+(\d+)", run("pdfinfo", str(pdf))).group(1))
    figures, text_parts = {}, []
    for p in range(1, pages + 1):
        t = run("pdftotext", "-layout", "-f", str(p), "-l", str(p), str(pdf), "-")
        text_parts.append(f"\n===== page {p} =====\n{t}")
        for m in CAPTION.finditer(t):
            figures.setdefault(p, set()).add(int(m.group(2)))
    (out / "text.txt").write_text("".join(text_parts))

    image_pages = set()
    for line in run("pdfimages", "-list", str(pdf)).splitlines()[2:]:
        parts = line.split()
        if parts and parts[0].isdigit():
            image_pages.add(int(parts[0]))

    to_render = range(1, pages + 1) if a.all else sorted(set(figures) | image_pages)
    for p in to_render:
        run("pdftoppm", "-png", "-r", str(a.dpi), "-f", str(p), "-l", str(p), "-singlefile", str(pdf), str(out / f"p-{p:02d}"))

    print(f"{pdf.relative_to(ROOT) if pdf.is_relative_to(ROOT) else pdf}: {pages} pages; text in text.txt")
    for p in sorted(set(figures) | image_pages):
        what = ", ".join(f"Fig. {n}" for n in sorted(figures.get(p, ()))) or "embedded image, no caption found"
        print(f"  page {p}: {what} -> p-{p:02d}.png")
    print("Vector figures with no caption on their own page are missed; check text.txt for 'Figure' if in doubt.")


if __name__ == "__main__":
    main()
