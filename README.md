# add-trial

A Claude Code plugin that reads a clinical-trial reference attachment (PDF, slide deck, or images), creates a fully structured entry in the right Notion oncology database — **Early Stage Cancer Database** or **Metastatic Cancer Database** — and keeps a study flashcard deck in sync with both.

## What's in here

| Piece | What it does |
| --- | --- |
| `skills/add-trial` | Reads the source, routes the trial, creates the Notion page, then triggers a flashcard |
| `agents/flashcard-writer` | Subagent that turns Notion rows into flashcards and republishes the deck |
| `commands/sync-flashcards` | `/sync-flashcards` — on-demand catch-up for edits made directly in Notion |
| `deck/` | The deck: card data, the artifact page, the offline build, sync state, and the diff tool |

## Workflow

1. Reads the uploaded source material directly (PDFs/images) and extracts key trial data.
2. **Routes the trial to the correct database** based on disease setting: localized stage I–III with curative intent (neoadjuvant/adjuvant/peri-operative) goes to the early-stage DB; advanced/metastatic disease treated with palliative intent goes to the metastatic DB. Ambiguous cases stop and ask.
3. Fetches the target data source's live schema and maps the data to it. The two databases have **different** schemas — e.g. the early-stage DB has `Timing`, `Number`, `DFS`, `pCR (%)` and `Completion (%)`, while the metastatic DB has `Line` and ORR/CR/PR/SD/DCR.
4. Creates a new Notion page with all properties filled and a detailed narrative body (Trial Design → Patient Population → Treatment → Results → Discussion → Reference), including a mandatory key efficacy results table.
5. Re-fetches the page to verify nothing was silently dropped, then reports what was inferred or left blank.
6. Hands the new page URL to the **flashcard-writer** subagent, which writes one flashcard and republishes the deck.

## Usage

Invoke it in Claude Code with `/add-trial <trial-name>`, or say:

- "Add this trial to Notion"
- "Summarize this trial into the database"

Attach the trial PDF, exported slide deck (PDF preferred), or screenshots before running.

## The flashcard deck

Every trial in the two databases is also a flashcard in **Trial Recall** — a two-stage study deck (identity → population/treatment/endpoints → takeaway) filterable by database, cancer type, setting and treatment class.

### Three ways to read the deck

| Copy | Where | Installs | Offline | Updates itself |
| --- | --- | --- | --- | --- |
| **Installed app** | GitHub Pages, from `docs/` | yes, own icon and name | yes, via service worker | yes, on each sync push |
| **Artifact** | claude.ai | no — see below | no | yes |
| **Offline file** | `deck/trial-recall-offline.html` | yes, once saved locally | yes | no, replace it by hand |

The artifact cannot be installed with its own icon: it renders inside a
sandboxed frame on claude.ai, and iOS reads home-screen metadata from the
top-level page. The deck's **Add to device** button detects this and offers the
routes that do work.

Both offline copies are built from `deck/trials.json`:

```bash
python3 deck/build.py          # rebuilds deck/trial-recall-offline.html and docs/
python3 deck/build.py --icons  # also redraws the app icons
```

`docs/` is what GitHub Pages serves, so it has to be committed for the app to
update. The icons are drawn by a small pure-standard-library PNG writer in
`build.py` — there is no image dependency to install.

### Order and progress

Each launch continues the shuffled run you were in, at the card you stopped on.
When a run finishes — or you press **New run** — the deck reshuffles. Trials
added by a sync are mixed into the part of the run you have not reached yet, so
syncing never restarts you. Progress, filters and starred cards live in that
browser's local storage, so they are per-device and do not follow you between
your phone and your desktop.

The deck stays in sync three ways:

- **On add** — `/add-trial` cards each trial it creates, as its last step.
- **Weekly** — a scheduled Routine runs a full sync and only writes cards for trials that actually changed.
- **On demand** — `/sync-flashcards` for a full catch-up, or `/sync-flashcards <trial>` for one trial.

Notion cannot push events to Claude Code, so edits made directly in Notion reach the deck at the next weekly or on-demand sync, not instantly.

### How change detection works

`deck/sync.py` fingerprints the card-relevant fields of every Notion row and stores the hashes in `deck/deck.json`. A sync pulls both databases, diffs against those fingerprints, and writes cards only for what changed — so a quiet week costs almost nothing.

```bash
python3 deck/sync.py plan rows.json      # what changed since last sync
python3 deck/sync.py validate            # check trials.json is publishable
python3 deck/sync.py commit rows.json    # record fingerprints after a sync
```

A card is keyed on the **Notion page URL**, never the trial name — card names are expanded for readability (Notion `CM-274` → card `CheckMate-274`), and renaming a trial in Notion updates its card rather than creating a duplicate.

Cards are never deleted automatically. If a trial disappears from Notion, the sync reports it and waits — a short pull looks identical to a deletion.

## Requirements

- Claude Code with the Notion MCP integration connected (`mcp__Notion__*` tools available).
- Python 3 for `deck/sync.py` (standard library only).
- A Notion workspace with both databases under the **Oncology Database** page:
  - **Early Stage Cancer Database** — data source id `2a312797-0a62-81c7-82ef-000b4de44d4b`
  - **Metastatic Cancer Database** — data source id `2a012797-0a62-81ff-b9bc-000b1334cb16`

## Schema

**Early Stage Cancer Database**
Select/multi-select: `Phase`, `Timing` (Peri-OP/Neoadjuvant/Adjuvant), `Cancer type` (single select), `Treatment` (incl. `Others`), `Biomarker`
Text/number: `Year`, `Number`, `Drug/Control`, `Patient population`, `DFS`, `PFS`, `OS`, `HR (95% CI)`, `pCR (%)`, `Completion (%)`, `>= Gr. 3 TRAE`, `Key takeaway`

**Metastatic Cancer Database**
Multi-select: `Phase`, `Line`, `Cancer type`, `Treatments`, `Biomarker`
Text/number: `Year`, `Drug/Control`, `Patient population`, `mOS (month)`, `PFS (month)`, `HR (95% CI)`, `ORR (%)`, `CR (%)`, `PR (%)`, `SD (%)`, `DCR (%)`, `>= Gr. 3 TRAE`, `Key takeaway`

See [`skills/add-trial/SKILL.md`](skills/add-trial/SKILL.md) for the routing rules, full schemas, value conventions, and page body template.

## Notes

- The Notion MCP tools do not support file uploads, so the original PDF/slide deck must be attached manually in Notion under the Reference section after the page is created.
- If a `.pptx` cannot be parsed directly, export it to PDF or paste key slide screenshots instead.
- Notion does not support `colspan`/`rowspan` in tables — it silently drops columns instead of erroring, so every row must have the same cell count. The skill verifies this after creating a page.
- Notion rejects unknown multi-select option values rather than creating them; the skill leaves the property blank and flags it instead of forcing a wrong label. Adding an option replaces the whole option set, so every existing option and colour must be restated.
- SQL queries against a data source return at most 100 rows; both databases are larger, so a full sync pages from both ends and de-duplicates on `url`. A short pull is indistinguishable from mass deletion, which is why the sync never deletes on its own.
- `deck/trial-recall-offline.html` and everything in `docs/` are build outputs of `deck/trials.json`; regenerate with `deck/build.py` rather than editing them by hand.
- Moving a trial between databases leaves its flashcard filed under the old one — re-run the flashcard-writer on that page after a move.
- A trial filed in the wrong database should be **moved**, not recreated — see "Correcting a mis-routed page" in the skill. Note that moving a page carries its old properties along and Notion silently adds matching columns to the destination database, so the destination schema must be re-checked and cleaned up afterwards.
