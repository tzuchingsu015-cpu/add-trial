#!/usr/bin/env python3
"""Build every distributable form of the Trial Recall deck.

  python3 deck/build.py

Produces, from deck/trial-recall.html + deck/trials.json:

  deck/trial-recall-offline.html   one self-contained file; no network, no account
  docs/                            the installable web app, served by GitHub Pages

Run it after every sync that changed a card, or both copies go stale while the
artifact stays current.

Pure standard library: no Pillow, so the icons are drawn by the small PNG
writer below rather than by an imaging package.
"""

import json
import hashlib
import math
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PAGE = ROOT / "trial-recall.html"
CARDS = ROOT / "trials.json"
OFFLINE = ROOT / "trial-recall-offline.html"
DOCS = REPO / "docs"

INK = (17, 23, 27)
TEAL = (25, 179, 154)
PLUM = (140, 58, 107)


# ---------------------------------------------------------------- PNG writer
def png(path, w, h, rows):
    """rows: list of h lists of w (r,g,b) tuples."""
    raw = bytearray()
    for row in rows:
        raw.append(0)                                   # filter type 0
        for r, g, b in row:
            raw += bytes((r, g, b))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    out += chunk(b"IEND", b"")
    path.write_bytes(out)


def in_round_rect(x, y, hw, hh, r):
    ax, ay = abs(x), abs(y)
    if ax > hw or ay > hh:
        return False
    dx, dy = ax - (hw - r), ay - (hh - r)
    if dx <= 0 or dy <= 0:
        return True
    return dx * dx + dy * dy <= r * r


def draw_icon(path, size):
    """Two offset cards on a dark ground — the deck's two halves."""
    ss = 2                                              # supersample for edges
    n = size * ss
    shapes = [                                          # (cx, cy, hw, hh, rot, colour)
        (0.44, 0.50, 0.20, 0.26, -0.18, PLUM),
        (0.57, 0.50, 0.20, 0.26, 0.12, TEAL),
    ]
    bg_r = 0.22 * n
    acc = [[(0, 0, 0)] * size for _ in range(size)]
    counts = [[0] * size for _ in range(size)]
    sums = [[[0, 0, 0] for _ in range(size)] for _ in range(size)]

    for py in range(n):
        y = py + 0.5
        for px in range(n):
            x = px + 0.5
            col = None
            if in_round_rect(x - n / 2, y - n / 2, n / 2, n / 2, bg_r):
                col = INK
                for cx, cy, hw, hh, rot, c in shapes:
                    ox, oy = x - cx * n, y - cy * n
                    ca, sa = math.cos(-rot), math.sin(-rot)
                    rx, ry = ox * ca - oy * sa, ox * sa + oy * ca
                    if in_round_rect(rx, ry, hw * n, hh * n, 0.055 * n):
                        col = c
            if col is None:
                col = INK                                # outside the rounded ground
            gx, gy = px // ss, py // ss
            s = sums[gy][gx]
            s[0] += col[0]; s[1] += col[1]; s[2] += col[2]
            counts[gy][gx] += 1

    rows = []
    for gy in range(size):
        row = []
        for gx in range(size):
            c = counts[gy][gx] or 1
            s = sums[gy][gx]
            row.append((s[0] // c, s[1] // c, s[2] // c))
        rows.append(row)
    png(path, size, size, rows)
    acc = None


# ---------------------------------------------------------------- offline file
OFFLINE_HEAD = """<!doctype html>
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


def build_offline(page, cards):
    blob = json.dumps(cards, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (OFFLINE_HEAD
            + "<script>window.TRIAL_RECALL_DATA=" + blob + ";</script>\n"
            + page + "\n</body>\n</html>\n")
    OFFLINE.write_text(html, encoding="utf-8")
    return OFFLINE


# ---------------------------------------------------------------- pages build
PAGES_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Flashcards for the oncology trial databases">
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Trial Recall">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="application-name" content="Trial Recall">
<meta name="theme-color" content="#0d6e5f">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="icon-512.png">
<style>
:root{color-scheme:light dark}
body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}
img{max-width:100%}
[hidden]:not([hidden=until-found i]){display:none!important}
</style>
</head>
<body>
"""

SW_REG = """
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js", {scope: "./"}).catch(function () {});
  });
}
</script>
"""

SW = """/* Trial Recall service worker - build %(build)s
   Cache-first so the deck opens instantly and works with no connection, with a
   background refresh so a sync reaches you on the next launch. */
var CACHE = "trial-recall-%(build)s";
var SHELL = ["./", "index.html", "trials.json", "manifest.webmanifest",
             "icon-180.png", "icon-192.png", "icon-512.png"];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    return c.addAll(SHELL);
  }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.map(function (k) {
      if (k !== CACHE) return caches.delete(k);
    }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  e.respondWith(caches.match(req).then(function (hit) {
    var net = fetch(req).then(function (res) {
      if (res && res.status === 200 && (res.type === "basic" || res.type === "cors")) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    }).catch(function () { return hit; });
    return hit || net;          /* cached wins for speed; network refills behind it */
  }));
});
"""

MANIFEST = {
    "name": "Trial Recall",
    "short_name": "Trial Recall",
    "description": "Flashcards for the oncology trial databases",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#eceff1",
    "theme_color": "#0d6e5f",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-180.png", "sizes": "180x180", "type": "image/png", "purpose": "any"},
    ],
}


def build_pages(page, cards, raw_cards):
    DOCS.mkdir(exist_ok=True)
    build = hashlib.sha1((raw_cards + page).encode("utf-8")).hexdigest()[:10]

    (DOCS / "index.html").write_text(
        PAGES_HEAD + page + SW_REG + "\n</body>\n</html>\n", encoding="utf-8")
    (DOCS / "trials.json").write_text(
        json.dumps(cards, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (DOCS / "manifest.webmanifest").write_text(
        json.dumps(MANIFEST, indent=2), encoding="utf-8")
    (DOCS / "sw.js").write_text(SW % {"build": build}, encoding="utf-8")
    # tells GitHub Pages not to run the files through Jekyll
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    for size in (180, 192, 512):
        f = DOCS / ("icon-%d.png" % size)
        if not f.exists() or "--icons" in sys.argv:
            draw_icon(f, size)
    return build


def main():
    if not PAGE.exists() or not CARDS.exists():
        print("missing deck/trial-recall.html or deck/trials.json")
        return 1
    page = PAGE.read_text(encoding="utf-8")
    raw = CARDS.read_text(encoding="utf-8")
    cards = json.loads(raw)

    if "TRIAL_RECALL_DATA" not in page:
        print("FAIL trial-recall.html has no window.TRIAL_RECALL_DATA branch; "
              "the offline build would fetch trials.json and fail")
        return 1

    build_offline(page, cards)
    build = build_pages(page, cards, raw)

    print("offline  deck/trial-recall-offline.html  %.0f KB" % (OFFLINE.stat().st_size / 1024))
    print("pages    docs/  (build %s)" % build)
    for f in sorted(DOCS.iterdir()):
        if f.name != ".nojekyll":
            print("           %-24s %6.0f KB" % (f.name, f.stat().st_size / 1024))
    print("%d cards" % len(cards))
    return 0


if __name__ == "__main__":
    sys.exit(main())
