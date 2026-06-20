# add-trial

A Claude Code skill that reads a clinical-trial reference attachment (PDF, slide deck, or images) and creates a fully structured entry in a Notion **Metastatic Cancer Database**.

## Workflow

1. Reads the uploaded source material directly (PDFs/images) and extracts key trial data.
2. Maps the data to a fixed property schema (Phase, Line, Cancer type, Treatments, Biomarker, survival outcomes, safety, etc.).
3. Creates a new Notion page with all properties filled and a detailed narrative body (Trial Design → Patient Population → Treatment → Results → Discussion → Reference), including a mandatory key efficacy results table.

## Usage

Invoke it in Claude Code with `/add-trial <trial-name>`, or say:

- "Add this trial to Notion"
- "Summarize this trial into the database"

Attach the trial PDF, exported slide deck (PDF preferred), or screenshots before running.

## Requirements

- Claude Code with the Notion MCP integration connected (`mcp__claude_ai_Notion__*` tools available).
- A Notion workspace with the **Metastatic Cancer Database** (data source id `2a012797-0a62-81ff-b9bc-000b1334cb16`).

## Schema

Multi-select fields: `Phase`, `Line`, `Cancer type`, `Treatments`, `Biomarker`  
Text/number fields: `Year`, `Drug/Control`, `Patient population`, `mOS (month)`, `PFS (month)`, `HR (95% CI)`, `ORR (%)`, `CR (%)`, `PR (%)`, `SD (%)`, `DCR (%)`, `>= Gr. 3 TRAE`, `Key takeaway`

See [`skills/add-trial/SKILL.md`](skills/add-trial/SKILL.md) for the full schema, value conventions, and page body template.

## Notes

- The Notion MCP tools do not support file uploads, so the original PDF/slide deck must be attached manually in Notion under the Reference section after the page is created.
- If a `.pptx` cannot be parsed directly, export it to PDF or paste key slide screenshots instead.
