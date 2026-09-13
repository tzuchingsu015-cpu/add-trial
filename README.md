# add-trial

A Claude Code skill that reads a clinical-trial reference attachment (PDF, slide deck, or images) and creates a fully structured entry in the right Notion oncology database — **Early Stage Cancer Database** or **Metastatic Cancer Database**.

## Workflow

1. Reads the uploaded source material directly (PDFs/images) and extracts key trial data.
2. **Routes the trial to the correct database** based on disease setting: localized stage I–III with curative intent (neoadjuvant/adjuvant/peri-operative) goes to the early-stage DB; advanced/metastatic disease treated with palliative intent goes to the metastatic DB. Ambiguous cases stop and ask.
3. Fetches the target data source's live schema and maps the data to it. The two databases have **different** schemas — e.g. the early-stage DB has `Timing`, `Number`, `DFS`, `pCR (%)` and `Completion (%)`, while the metastatic DB has `Line` and ORR/CR/PR/SD/DCR.
4. Creates a new Notion page with **concise** properties and a detailed narrative body (Trial Design → Patient Population → Treatment → Results → Discussion → Reference), including a mandatory key efficacy results table. The split is deliberate: properties stay scannable, the body carries the depth.
5. Re-fetches the page to verify nothing was silently dropped, then reports what was inferred or left blank.

## Usage

Invoke it in Claude Code with `/add-trial <trial-name>`, or say:

- "Add this trial to Notion"
- "Summarize this trial into the database"

Attach the trial PDF, exported slide deck (PDF preferred), or screenshots before running.

## Requirements

- Claude Code with the Notion MCP integration connected (`mcp__Notion__*` tools available).
- A Notion workspace with both databases under the **Oncology Database** page:
  - **Early Stage Cancer Database** — data source id `2a312797-0a62-81c7-82ef-000b4de44d4b`
  - **Metastatic Cancer Database** — data source id `2a012797-0a62-81ff-b9bc-000b1334cb16`

## Schema

**Early Stage Cancer Database**
Select/multi-select: `Phase`, `Timing` (Peri-OP/Neoadjuvant/Adjuvant), `Cancer type` (multi-select — see Notes), `Treatment` (incl. `Others`), `Biomarker`
Text/number: `Year`, `Number`, `Drug/Control`, `Patient population`, `DFS`, `PFS`, `OS`, `HR (95% CI)`, `pCR (%)`, `Completion (%)`, `>= Gr. 3 TRAE`, `Key takeaway`

**Metastatic Cancer Database**
Multi-select: `Phase`, `Line`, `Cancer type`, `Treatments`, `Biomarker`
Text/number: `Year`, `Drug/Control`, `Patient population`, `mOS (month)`, `PFS (month)`, `HR (95% CI)`, `ORR (%)`, `CR (%)`, `PR (%)`, `SD (%)`, `DCR (%)`, `>= Gr. 3 TRAE`, `Key takeaway`

### Property conventions

Properties are a scannable table row, not the write-up:

- Each property carries only its **key** reportable items — key inclusion/exclusion criteria; the demographics that matter across trials in the same setting; the primary and key secondary endpoints; only those subgroups the article itself emphasises; the differentiating toxicities and treatment-related deaths; and a 3–5 line `Key takeaway`. Everything else belongs in the page body.
- **Confidence intervals appear only on hazard ratios**, i.e. only in `HR (95% CI)`. Medians, percentages and rates carry the point estimate plus a P value where it matters. An HR quoted outside that property is written `HR x.xx; P=y`, with no CI.
- A convention change applies to **new entries only** — existing pages are not retroactively rewritten unless explicitly requested.

See [`skills/add-trial/SKILL.md`](skills/add-trial/SKILL.md) for the routing rules, full schemas, value conventions, and page body template.

## Notes

- The Notion MCP tools do not support file uploads, so the original PDF/slide deck must be attached manually in Notion under the Reference section after the page is created.
- If a `.pptx` cannot be parsed directly, export it to PDF or paste key slide screenshots instead.
- Notion does not support `colspan`/`rowspan` in tables — it silently drops columns instead of erroring, so every row must have the same cell count. The skill verifies this after creating a page.
- Notion rejects unknown multi-select option values rather than creating them; the skill leaves the property blank and flags it instead of forcing a wrong label. Adding an option replaces the whole option set, so every existing option and colour must be restated.
- `Cancer type` is **`multi_select` in both databases** and must be passed as an array. It was a single `select` in the early-stage DB until a page move from the metastatic DB flipped its type. Always check the live schema before mapping — this is exactly the kind of drift the fetch-schema-first step exists to catch.
- A trial filed in the wrong database should be **moved**, not recreated — see "Correcting a mis-routed page" in the skill. Note that moving a page carries its old properties along and Notion silently adds matching columns to the destination database, so the destination schema must be re-checked and cleaned up afterwards.
