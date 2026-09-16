#!/usr/bin/env python3
"""Build a single self-contained Trial Recall file.

  python3 deck/build-standalone.py

Reads deck/trial-recall.html + deck/trials.json and writes
deck/trial-recall-offline.html: the same deck with the card data inlined and
a real <head>, so it opens straight from the filesystem with no sign-in, no
network and no artifact hosting.

Regenerate it after every sync, or the offline copy silently goes stale.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGE = ROOT / "trial-recall.html"
CARDS = ROOT / "trials.json"
OUT = ROOT / "trial-recall-offline.html"

# The published artifact gets its <head> injected at publish time; a file on
# disk has no such wrapper, so supply the equivalent here.
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Trial Recall">
<meta name="theme-color" content="#0d6e5f">
<style>
:root{color-scheme:light dark}
body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}
img{max-width:100%}
[hidden]:not([hidden=until-found i]){display:none!important}
</style>
</head>
<body>
"""

FOOT = "\n</body>\n</html>\n"


def main():
    if not PAGE.exists() or not CARDS.exists():
        print("missing deck/trial-recall.html or deck/trials.json")
        return 1

    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")

    # </script> inside a JSON string would close the tag we are writing into.
    blob = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    blob = blob.replace("</", "<\\/")

    inline = ('<script>window.TRIAL_RECALL_DATA=' + blob + ';</script>\n')

    # The page boots from window.TRIAL_RECALL_DATA when present, so the data
    # only has to be defined before the page script runs.
    html = HEAD + inline + page + FOOT
    OUT.write_text(html, encoding="utf-8")

    kb = OUT.stat().st_size / 1024
    print("wrote %s  (%d cards, %.0f KB)" % (OUT.relative_to(ROOT.parent), len(cards), kb))
    if "TRIAL_RECALL_DATA" not in page:
        print("WARNING: trial-recall.html has no window.TRIAL_RECALL_DATA branch; "
              "the offline build will try to fetch trials.json and fail")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
