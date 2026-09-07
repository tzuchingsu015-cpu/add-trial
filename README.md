# add-trial

Two Claude Code skills for oncology reference work.

- **`add-trial`** — reads a clinical-trial reference attachment (PDF, slide deck, or images) and creates a fully structured entry in a Notion **Metastatic Cancer Database**.
- **`nccn-summary`** — isolates one disease subset of an NCCN guideline into an HTML artifact where every algorithm recommendation carries the Discussion evidence and rationale behind it.

## add-trial

### Workflow

1. Reads the uploaded source material directly (PDFs/images) and extracts key trial data.
2. Maps the data to a fixed property schema (Phase, Line, Cancer type, Treatments, Biomarker, survival outcomes, safety, etc.).
3. Creates a new Notion page with all properties filled and a detailed narrative body (Trial Design → Patient Population → Treatment → Results → Discussion → Reference), including a mandatory key efficacy results table.

### Usage

Invoke it in Claude Code with `/add-trial <trial-name>`, or say:

- "Add this trial to Notion"
- "Summarize this trial into the database"

Attach the trial PDF, exported slide deck (PDF preferred), or screenshots before running.

### Requirements

- Claude Code with the Notion MCP integration connected (`mcp__claude_ai_Notion__*` tools available).
- A Notion workspace with the **Metastatic Cancer Database** (data source id `2a012797-0a62-81ff-b9bc-000b1334cb16`).

### Schema

Multi-select fields: `Phase`, `Line`, `Cancer type`, `Treatments`, `Biomarker`  
Text/number fields: `Year`, `Drug/Control`, `Patient population`, `mOS (month)`, `PFS (month)`, `HR (95% CI)`, `ORR (%)`, `CR (%)`, `PR (%)`, `SD (%)`, `DCR (%)`, `>= Gr. 3 TRAE`, `Key takeaway`

See [`skills/add-trial/SKILL.md`](skills/add-trial/SKILL.md) for the full schema, value conventions, and page body template.

### Notes

- The Notion MCP tools do not support file uploads, so the original PDF/slide deck must be attached manually in Notion under the Reference section after the page is created.
- If a `.pptx` cannot be parsed directly, export it to PDF or paste key slide screenshots instead.

## nccn-summary

NCCN guidelines separate the *recommendation* from the *reason*: the algorithm pages (BINV-n, COL-n, REC-n) give the decision boxes and citation superscripts with no results, while the Discussion (MS-n) carries the trials, the numbers, the negative studies, and the panel's reasoning. A summary built from the algorithm alone gives only the conclusion.

This skill pairs them. For every decision node it carries over, it goes and finds the matching Discussion passage and attaches two things: what the trials showed, and why the recommendation is worded the way it is — why a hedge, why a category 2B, why an alternative option is offered, why a cutoff sits where it does.

### Usage

Invoke with `/nccn-summary <disease subset>`, or say:

- "Isolate the early HR-positive breast cancer part of this guideline"
- "Summarize the BINV section, split into preoperative and adjuvant"

Supply the guideline PDF, or a Google Drive link to one.

### What it produces

An HTML artifact with the scope and version stated up front, a compressed decision path, a node-by-node rationale section, treatment broken down by class, a trial index (name, population, efficacy result), and a list of places where the algorithm has moved past its own Discussion.

### Notes

- Every efficacy figure is badged to the guideline page it came from, or explicitly marked as unverified primary-literature recall.
- The Discussion is revised on its own cycle and can lag the algorithm pages by more than a year; the skill flags those divergences with both dates rather than silently picking one.
- `scripts/extract_columns.py` handles the two-column Discussion layout, which ordinary PDF text extraction interleaves into unreadable output. Requires `pymupdf`.

See [`skills/nccn-summary/SKILL.md`](skills/nccn-summary/SKILL.md) for the full method.
