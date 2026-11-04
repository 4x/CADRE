"""Crude stdlib-only PDF text scraper for reviewer source verification.

Decompresses FlateDecode content streams and concatenates text-showing
string operands. Good enough to confirm figure/table presence and formula
wording; not a general PDF reader. Usage:
  uv run --no-env-file python ingest-notes/slice-e-work/pdfextract.py <pdf>
"""

import re
import sys
import zlib


def extract(path):
    """Return scraped text from Flate streams plus raw string operands."""
    raw = open(path, "rb").read()
    texts = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        blob = m.group(1)
        try:
            dec = zlib.decompress(blob)
        except Exception:  # noqa: BLE001
            continue
        for t in re.findall(rb"\((?:[^()\\]|\\.)*\)", dec):
            s = t[1:-1].decode("latin-1")
            s = re.sub(r"\\([()\\])", r"\1", s)
            texts.append(s)
    return " ".join(texts)


if __name__ == "__main__":
    out = extract(sys.argv[1])
    sys.stdout.write(out.encode("ascii", "replace").decode("ascii"))
    sys.stdout.write(f"\n[CHARS={len(out)}]\n")
