# add-trial

A Claude Code skill that reads a clinical-trial reference attachment (PDF, slide deck, or images) and creates a fully structured entry in the correct Notion clinical-trial database.

## Workflow

1. Reads the uploaded source material directly (PDFs/images) and extracts key trial data.
2. Routes the trial to the correct database by disease setting: adjuvant/neoadjuvant/peri-operative trials go to the **Early Stage Cancer Database**, metastatic/advanced trials go to the **Metastatic Cancer Database**. See [`skills/add-trial/DATABASES.md`](skills/add-trial/DATABASES.md).
3. Maps the data to that database's property schema (Phase, Cancer type, Treatments, Biomarker, survival outcomes, safety, etc.).
4. Checks for an existing page with the same trial name before creating, to avoid duplicates.
5. Creates a new Notion page with all properties filled and a detailed narrative body (Trial Design → Patient Population → Treatment → Results → Discussion → Reference), including a mandatory key efficacy results table.

## Usage

Invoke it in Claude Code with `/add-trial <trial-name>`, or say:

- "Add this trial to Notion"
- "Summarize this trial into the database"

Attach the trial PDF, exported slide deck (PDF preferred), or screenshots before running.

## Requirements

- Claude Code with the Notion MCP integration connected (`mcp__claude_ai_Notion__*` tools available).
- A Notion workspace with both databases:
  - **Early Stage Cancer Database** (data source id `2a312797-0a62-81c7-82ef-000b4de44d4b`)
  - **Metastatic Cancer Database** (data source id `2a012797-0a62-81ff-b9bc-000b1334cb16`)

## Schema

Each database has its own schema — see [`skills/add-trial/DATABASES.md`](skills/add-trial/DATABASES.md) for the full field list per database, and [`skills/add-trial/SKILL.md`](skills/add-trial/SKILL.md) for value conventions and the page body template.

Metastatic DB multi-select fields: `Phase`, `Line`, `Cancer type`, `Treatments`, `Biomarker`  
Metastatic DB text/number fields: `Year`, `Drug/Control`, `Patient population`, `mOS (month)`, `PFS (month)`, `HR (95% CI)`, `ORR (%)`, `CR (%)`, `PR (%)`, `SD (%)`, `DCR (%)`, `>= Gr. 3 TRAE`, `Key takeaway`

## Notes

- The Notion MCP tools do not support file uploads, so the original PDF/slide deck must be attached manually in Notion under the Reference section after the page is created.
- If a `.pptx` cannot be parsed directly, export it to PDF or paste key slide screenshots instead.
- Notion database schema/settings (properties, views) are protected: `.claude/settings.json` denies creating databases/views and denies renaming views, and requires explicit confirmation (`ask`) before any data-source/property edit — this skill should never restructure a database's schema on its own.
