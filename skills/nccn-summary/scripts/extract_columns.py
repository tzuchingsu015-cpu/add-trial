#!/usr/bin/env python3
"""Column-aware text extraction for NCCN guideline PDFs.

NCCN Discussion (MS-n) pages are two-column. PyMuPDF's ordinary text
extraction — including get_text('text', sort=True) — interleaves the two
columns line by line and produces unreadable output. This splits lines by
the midpoint of their bounding box against the page centre, emits the left
column in full and then the right, and strips the repeating page furniture
(EULA notice, "Printed by ..." watermark, version stamp, running heads).

Usage:
    python3 extract_columns.py <pdf> <first-page> <last-page> [--offset N]

Pages are 0-based PDF indices (as PyMuPDF numbers them), last exclusive.
--offset N prints a friendly "MS-x" label alongside each page, where
x = pdf_index - N. Find N by locating MS-1 once: in Breast Cancer v6.2026
MS-1 was PDF index 127, so --offset 126.

Requires: pip install pymupdf
"""

import argparse
import re
import sys

import pymupdf

# Repeating page furniture. Everything here is guideline boilerplate, not
# content; dropping it keeps the extracted text readable and keeps verbatim
# guideline text out of the working notes.
FURNITURE = [
    r"PLEASE NOTE that use of this NCCN Content.*",
    r"Printed by .*",
    r"Version \d+\.\d{4} © \d{4} National.*",
    r"^NCCN Guidelines Version \d+\.\d{4}.*$",
    r"^NCCN Guidelines Index.*$",
    r"^Table of Contents.*$",
    r"^Discussion\s*$",
    r"^MS-\d+\s*$",
]


def page_text(doc, i):
    page = doc[i]
    width = page.rect.width
    left, right = [], []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            txt = "".join(s["text"] for s in line["spans"]).rstrip()
            if not txt.strip():
                continue
            x0, y0, x1, _ = line["bbox"]
            (left if (x0 + x1) / 2 < width / 2 else right).append((y0, x0, txt))
    out = []
    for col in (left, right):
        col.sort(key=lambda r: (round(r[0], 1), r[1]))
        out.append("\n".join(t for _, _, t in col))
    return "\n".join(out)


def clean(text):
    for pat in FURNITURE:
        text = re.sub(pat, "", text, flags=re.M)
    return re.sub(r"\n{2,}", "\n", text).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("first", type=int)
    ap.add_argument("last", type=int)
    ap.add_argument("--offset", type=int, default=None,
                    help="pdf_index - offset = MS number, for labelling")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    last = min(args.last, doc.page_count)
    for i in range(args.first, last):
        label = f"MS-{i - args.offset}" if args.offset is not None else f"page"
        print(f"\n########## {label} (pdf {i}) ##########")
        print(clean(page_text(doc, i)))


if __name__ == "__main__":
    sys.exit(main())
