# add-trial

A Claude Code skill that reads a clinical-trial reference attachment (PDF, slide
deck, or images) and creates a fully structured entry in a Notion clinical-trial
database — with a per-endpoint efficacy verdict applied automatically.

## Workflow

1. Reads the uploaded source material directly (PDFs/images) and extracts key trial data.
2. Maps the data to a fixed property schema (Phase, Line, Cancer type, Treatments, Biomarker, survival outcomes, safety, etc.).
3. **Applies an efficacy verdict symbol to every result line** (see below).
4. Creates a new Notion page with all properties filled and a detailed narrative body (Trial Design → Patient Population → Treatment → Results → Discussion → Reference), including a mandatory key efficacy results table.

## Usage

Invoke it in Claude Code with `/add-trial <trial-name>`, or say:

- "Add this trial to Notion"
- "Summarize this trial into the database"

Attach the trial PDF, exported slide deck (PDF preferred), or screenshots before running.

## Efficacy result symbols

Every efficacy outcome value is prefixed with a verdict symbol so the table view
shows at a glance whether each endpoint was positive. Symbols are applied **per
result line, never per trial** — a single row can carry several.

| Symbol | Meaning |
|---|---|
| ✅ | Statistically significant benefit — the endpoint met **its own prespecified boundary** |
| ⚠️ | Failed its own test, was never formally tested, or is immature |
| ❌ | No benefit, endpoint not met, or the control arm did better |
| **↔** | **Non-inferiority met** — the endpoint was powered to show "not worse", so an HR near 1 is a success |
| *(none)* | Single-arm trials, rows with no efficacy data, and analyses that are not treatment comparisons |

Three rules do most of the work:

- **The trial's own alpha decides, not `p < 0.05` and not the CI bound.** A CI
  resting on 1.00 is ✅ when the boundary was met (FLAURA, p=0.046 vs α=0.0495);
  a CI that clears 1 is ⚠️ when the trial never formally tested it (KEYNOTE-177)
  or missed its position in the testing hierarchy (KEYNOTE-355, α=0.00111).
- **Response endpoints are marked only where a test exists.** ORR, DCR and pCR
  get a symbol only when a p-value, odds ratio, or CI on the *difference* is
  reported. A bare response rate is left unmarked rather than guessed at.
- **Check the direction before marking.** Verify which arm the hazard ratio is
  written for, that the arm order matches `Drug/Control`, and whether the
  statistic is really an odds ratio (where > 1 is favourable). If the medians and
  the HR disagree, leave the cell unmarked and flag it.

`skills/add-trial/SKILL.md` carries the full convention, including the five
direction traps that produced wrong verdicts on a first mechanical pass.

## Requirements

- Claude Code with the Notion MCP integration connected (`mcp__Notion__notion-fetch`, `mcp__Notion__notion-update-page`, `mcp__Notion__notion-query-data-sources`, etc. available).
- A Notion workspace containing:
  - **Metastatic Cancer Database** — data source id `2a012797-0a62-81ff-b9bc-000b1334cb16`
  - **Early Stage Cancer Database** — data source id `2a312797-0a62-81c7-82ef-000b4de44d4b`

## Schema

**Metastatic** — multi-select: `Phase`, `Line`, `Cancer type`, `Treatments`, `Biomarker`.
Text/number: `Year`, `Drug/Control`, `Patient population`, `mOS (month)`, `PFS (month)`,
`HR (95% CI)`, `ORR (%)`, `CR (%)`, `PR (%)`, `SD (%)`, `DCR (%)`, `>= Gr. 3 TRAE`, `Key takeaway`.

**Early stage** — a different schema: `"DFS "` (note the trailing space), `OS`, `PFS`,
`pCR (%)`, `HR (95% CI)`, `Completion (%)`. No `ORR`/`DCR`/`CR`/`PR`/`SD`.

Symbols go on the outcome and hazard-ratio properties only — never on `CR (%)`,
`PR (%)`, `SD (%)`, `>= Gr. 3 TRAE`, or `Completion (%)`.

See [`skills/add-trial/SKILL.md`](skills/add-trial/SKILL.md) for the full schema,
value conventions, and page body template.

## Review reports

A full verdict pass has been completed across **both databases** — 103 metastatic
rows and 45 early-stage rows carry per-endpoint symbols (11 early-stage rows are
deliberately unmarked: non-comparative designs, prognostic analyses, template and
empty rows). Two artefacts record what the pass found along the way:

- [`DATA_ISSUES_REVIEW.md`](DATA_ISSUES_REVIEW.md) — every data error and
  second-look item, ordered by how wrong the data is: conflicting values,
  statistically impossible CIs, mislabelled statistics, direction traps, missing
  statistics, typos, and structural problems. Includes a handful of open
  questions (verdicts to confirm, one rule conflict) that only the database
  owner can settle.
- `Oncology_DB_data_issues.xlsx` — the same register as a working spreadsheet,
  with a Status column for tracking fixes, plus tabs for verdicts to confirm,
  the open rule decision, deliberately unmarked rows, and non-inferiority designs.

## Notes

- The Notion MCP tools do not support file uploads, so the original PDF/slide deck must be attached manually in Notion under the Reference section after the page is created.
- If a `.pptx` cannot be parsed directly, export it to PDF or paste key slide screenshots instead.
- **Never build a Notion update from `notion-query-data-sources` output.** SQL
  results are plain text and silently strip `**bold**`, colour spans, and
  `discussion://` comment anchors. Fetch the page with `notion-fetch` and write
  from that markdown instead.
