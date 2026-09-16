#!/usr/bin/env python3
"""Deck bookkeeping for the Trial Recall flashcards.

The flashcard-writer subagent uses this so it only spends effort on trials that
actually changed, instead of re-reading both Notion databases every sync.

  plan     rows.json   what changed since the last sync (new / changed / gone)
  seed     rows.json   record current Notion state without reporting changes
  commit   rows.json   after cards are written: update fingerprints + timestamp
  validate             check deck/trials.json is well formed and publishable

rows.json is what the agent dumps straight out of the two Notion SQL queries:

  {"early": [ {...row...}, ... ], "met": [ {...row...}, ... ]}

Row keys are the Notion property names; only the ones that feed a card are
fingerprinted, so cosmetic edits elsewhere in the database do not churn the deck.

Identity is the Notion page `url`, never the trial name: card names are display
labels that get expanded for readability (Notion "CM-274" -> card
"CheckMate-274"), and a trial renamed in Notion must update its card, not spawn
a second one.
"""

import json
import hashlib
import sys
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CARDS = ROOT / "trials.json"
STATE = ROOT / "deck.json"

# Property names that actually feed a flashcard, per database.
SOURCE_FIELDS = {
    "early": ["name", "yr", "phase", "ca", "bm", "timing", "pop", "arms", "tx",
              "n", "pcr", "dfs", "pfs", "os", "hr", "takeaway"],
    "met":   ["name", "yr", "phase", "ca", "bm", "line", "pop", "arms", "tx",
              "orr", "dcr", "pfs", "os", "hr", "takeaway"],
}

CARD_KEYS = ["db", "name", "year", "phase", "cancer", "biomarker", "setting",
             "n", "population", "treatment", "tx", "endpoints", "takeaway", "url"]


def norm(v):
    """Whitespace-insensitive so a stray newline in Notion is not a 'change'."""
    if v is None:
        return None
    return " ".join(str(v).split())


def fingerprint(row, db):
    payload = json.dumps([norm(row.get(f)) for f in SOURCE_FIELDS[db]],
                         ensure_ascii=False)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def load_state():
    return json.loads(STATE.read_text(encoding="utf-8"))


def save_state(state):
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n",
                     encoding="utf-8")


def is_template(row):
    """Both databases keep a page template as a row; it is not a trial."""
    return norm(row.get("name") or "").lower().startswith("template for")


def load_rows(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = {}
    for db in ("early", "met"):
        for row in data.get(db, []):
            url = (row.get("url") or "").strip()
            if not url or is_template(row):
                continue
            out[url] = (db, row)
    return out


def cmd_plan(rows_path):
    state = load_state()
    old = state.get("fingerprints", {})
    rows = load_rows(rows_path)
    cards = {c["url"]: c for c in json.loads(CARDS.read_text(encoding="utf-8"))}

    new, changed, gone = [], [], []
    for url, (db, row) in sorted(rows.items(), key=lambda kv: kv[1][1].get("name") or ""):
        fp = fingerprint(row, db)
        if url not in cards:
            new.append((row.get("name"), db, url))
        elif old.get(url) != fp:
            changed.append((row.get("name"), db, url))
    for url, c in sorted(cards.items(), key=lambda kv: kv[1]["name"]):
        if url not in rows:
            gone.append("%s  %s" % (c["name"], url))

    print("last sync: %s" % state.get("last_synced_at", "never"))
    print("notion rows: %d   cards: %d" % (len(rows), len(cards)))
    print()
    for label, items in (("NEW", new), ("CHANGED", changed)):
        print("%s (%d)" % (label, len(items)))
        for name, db, url in items:
            print("  [%s] %s  %s" % (db, name, url))
        print()
    print("GONE FROM NOTION (%d) - do not delete without asking" % len(gone))
    for name in gone:
        print("  %s" % name)
    print()
    todo = len(new) + len(changed)
    print("=> %d card(s) to write. %d unchanged." % (todo, len(rows) - todo))
    return 0


def cmd_seed(rows_path):
    state = load_state()
    rows = load_rows(rows_path)
    state["fingerprints"] = {u: fingerprint(r, db) for u, (db, r) in rows.items()}
    state["last_synced_at"] = datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    save_state(state)
    print("seeded %d source fingerprints (keyed by notion url)"
          % len(state["fingerprints"]))
    return 0


def cmd_commit(rows_path):
    rc = cmd_validate()
    if rc:
        return rc
    state = load_state()
    rows = load_rows(rows_path)
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    state["fingerprints"] = {u: fingerprint(r, db) for u, (db, r) in rows.items()}
    state["card_count"] = len(cards)
    state["last_synced_at"] = datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    save_state(state)
    print("committed: %d cards, %d fingerprints, synced %s"
          % (len(cards), len(state["fingerprints"]), state["last_synced_at"]))
    return 0


def cmd_validate():
    try:
        cards = json.loads(CARDS.read_text(encoding="utf-8"))
    except Exception as exc:                      # noqa: BLE001
        print("FAIL trials.json is not valid JSON: %s" % exc)
        return 1

    problems = []
    seen = {}
    for idx, c in enumerate(cards):
        where = "card %d (%s)" % (idx, c.get("name", "<unnamed>"))
        missing = [k for k in CARD_KEYS if k not in c]
        if missing:
            problems.append("%s missing keys: %s" % (where, ", ".join(missing)))
        if c.get("db") not in ("early", "met"):
            problems.append("%s db must be 'early' or 'met'" % where)
        for k in ("name", "population", "treatment", "takeaway", "url",
                  "cancer", "setting"):
            if not str(c.get(k) or "").strip():
                problems.append("%s empty %s" % (where, k))
        if not isinstance(c.get("tx"), list):
            problems.append("%s tx must be a list" % where)
        eps = c.get("endpoints")
        if not isinstance(eps, list) or not eps:
            problems.append("%s endpoints must be a non-empty list" % where)
        else:
            for e in eps:
                if not (isinstance(e, list) and len(e) == 2
                        and all(isinstance(x, str) for x in e)):
                    problems.append("%s endpoint rows must be [label, value] "
                                    "string pairs" % where)
                    break
        if not str(c.get("url") or "").startswith("http"):
            problems.append("%s url must be a link to the Notion page" % where)
        url = c.get("url")
        if url in seen:
            problems.append("two cards share notion url %r (cards %d and %d) - "
                            "one trial, one card" % (url, seen[url], idx))
        seen[url] = idx

    if problems:
        print("FAIL %d problem(s):" % len(problems))
        for p in problems[:40]:
            print("  - %s" % p)
        if len(problems) > 40:
            print("  ... and %d more" % (len(problems) - 40))
        return 1

    early = sum(1 for c in cards if c["db"] == "early")
    print("OK %d cards (%d early, %d metastatic), no duplicate notion urls"
          % (len(cards), early, len(cards) - early))
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "validate":
        return cmd_validate()
    if cmd in ("plan", "seed", "commit"):
        if len(argv) < 3:
            print("%s needs a path to rows.json" % cmd)
            return 2
        return {"plan": cmd_plan, "seed": cmd_seed, "commit": cmd_commit}[cmd](argv[2])
    print("unknown command %r" % cmd)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
