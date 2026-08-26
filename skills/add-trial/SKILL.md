---
name: add-trial
description: Use when the user uploads clinical-trial reference attachments (PDF, slide deck, or images) and a trial name, and wants it added/summarized into the Notion "Metastatic Cancer Database". Trigger phrases: "add this trial to Notion", "summarize this trial into the database", "/add-trial".
argument-hint: <trial-name>
---

# Add Trial to Notion Metastatic Cancer Database

Summarizes a clinical trial from reference attachments (PDF, slide deck, or images)
into a new page in the Notion "Metastatic Cancer Database", filling structured
properties concisely and writing a detailed narrative summary in the page body.

## Target database

- Database: "Metastatic Cancer Database"
- Data source id (parent for new pages): `2a012797-0a62-81ff-b9bc-000b1334cb16`
- Title property: `Key Trials/Med`
- If the data source id no longer resolves, re-fetch it: search Notion for
  "Metastatic Cancer Database", fetch the result, and read the
  `<data-source url="collection://...">` id from the response.

## Schema reference

Multi-select properties — reuse an existing option label whenever the trial's
data matches one; only introduce a new label if nothing existing fits, and
flag that to the user in the final report.

- `Phase`: Retro, Ongoing, I, II, III
- `Line`: 1, 2, 3
- `Cancer type`: Other, Endometrial CA, Cerical CA, Ovary, Sarcoma, Skin, CRC,
  GC, Esophagus, UC, Pancreas, BTC, HCC, Breast, Lung, NPC, HEENT
- `Treatments`: NSAI, Anti-EGFR, SERD, CDK4/6i, Endocrine, RT, BsAb, Others,
  ADC, TKI, Anti-VEGF, ICI, ChT
- `Biomarker`: AKT, PIK3CA, HR, TP53, dMMR, RAF, RAS, RET, MET, ESR, ALK,
  ROS1, EGFR, HER2

Text/number properties: `Year` (number), `Drug/Control`, `Patient population`,
`mOS (month)`, `PFS (month)`, `HR (95% CI)`, `ORR (%)`, `CR (%)`, `PR (%)`,
`SD (%)`, `DCR (%)`, `>= Gr. 3 TRAE`, `Key takeaway`.

Property value conventions (match existing entries, e.g. MONARCH-2):
- Comparative arms as `"A vs B"` (e.g. PFS `"16.9 vs 9.3"`).
- `HR (95% CI)` as `value (lower-upper); P=x` (use `P<0.0001` style when given).
- Percentages as `"A% vs B%"`, optionally with population/year noted in
  parentheses when the source distinguishes them (e.g. `"83.0 vs 75.8 (CR+PR+SD, 2017)"`).
- `Key takeaway` is short, bolded, may use `<span color="red">...</span>` to
  highlight the key result.

### Efficacy result symbols

Prefix every efficacy **outcome** value with a verdict symbol so the database
view shows at a glance whether each endpoint was positive. Applies to
`PFS (month)`, `mOS (month)`, `ORR (%)`, `DCR (%)`, and `HR (95% CI)`:

- `✅` — statistically significant benefit (endpoint met; p below the
  prespecified boundary, or HR 95% CI excluding 1). A confidence interval
  whose bound sits **exactly on 1.00** still counts as `✅` when the trial
  reported the endpoint as met — see the borderline rule below.
- `⚠️` — numerically favorable but **not** statistically significant, not
  formally tested, or immature/unreported data.
- `❌` — no benefit, endpoint not met, or the control arm did better.
- `**↔**` (bold) — **non-inferiority met**. Use this, never `✅`/`❌`, whenever
  the endpoint was powered for non-inferiority rather than superiority: there
  the question was "is it not worse", so a hazard ratio near 1 is a *success*
  and both a check and a cross would misreport it. Applies per endpoint, not
  per trial — a trial can be `**↔**` on OS and `❌` on a superiority PFS
  endpoint in the same row.

Rules:
- One symbol per result line — if a property holds several populations
  (`Overall:` / `1L:` / `2L:` separated by `<br>`), each line gets its own
  symbol, since subgroups can differ from ITT.
- Judge the verdict from the trial's own statistics, not from the size of the
  numeric gap, and not from the CI bound alone.
- **Borderline CIs resting on 1.00 are `✅`, not `⚠️`.** A bound that rounds to
  1.00 (or sits a hundredth past it) does not by itself make a result
  negative — what matters is whether the trial met its own prespecified
  significance level and whether the effect is clinically meaningful. Two
  worked examples, both settled as `✅`:
    - FLAURA OS — HR 0.80 (0.64–**1.00**), p=0.046 against a prespecified
      alpha of 0.0495. The boundary was met; the trial reports OS as positive.
    - MONALEESA-3 OS in the 1L and 2L subsets — HR 0.70 (0.48–**1.02**) and
      0.73 (0.53–**1.00**), sitting under a significant ITT result
      (HR 0.72, P=0.00455) and pointing the same direction.
  Reserve `⚠️` for results that genuinely failed their own test — a p-value
  above the prespecified boundary (KEYNOTE-224/240, LEAP-002, EMERALD's
  interim OS), an untested or exploratory analysis, or immature data.
- Leave **single-arm trials completely unmarked**. With no comparator there is
  no verdict to report, and a symbol would imply a comparison that was never
  made. Same for rows with no efficacy data, template rows, and analyses that
  are not treatment comparisons (e.g. a pCR-vs-no-pCR prognostic association).
- Do **not** put symbols on `CR (%)`, `PR (%)`, `SD (%)`, or `>= Gr. 3 TRAE` —
  those are response components and safety data, not endpoints with a
  positive/negative verdict.
- `HR (95% CI)` is marked too, so each statistic line carries the same verdict
  as the outcome value it supports. Keep the symbols consistent between the two
  columns — a `✅` PFS value must not sit beside a `⚠️` PFS hazard ratio.
- Preserve any existing inline markup when adding a symbol to `HR (95% CI)`.
  Some cells wrap an endpoint label in `<span discussion-urls="...">`, which
  anchors a Notion comment; put the symbol **before** the span and copy the
  span through verbatim, or the comment is orphaned. The same applies to
  escaped characters such as `p\<0.0001`.
- The existing bold/yellow convention in `HR (95% CI)` still flags which
  endpoint was primary; the symbol reports whether it was met. They are
  independent — do not use one in place of the other.

## Page body structure

Reproduce this exact section structure (yellow background headers), written
with a **detailed** narrative — this is the one place to be thorough, in
contrast to the concise properties above:

```
# Trial Design {color="yellow_bg"}
---
- Design, N, randomization, stratification, endpoints (primary/secondary/exploratory)

# Patient Population {color="yellow_bg"}
---
- Population/eligibility, key exclusions, key demographics
(optional <details><summary>Detailed patient demographics</summary>...</details>)

# Treatment {color="yellow_bg"}
---
- Study group: dosing
- Control group: dosing

# Results {color="yellow_bg"}
---
## Key Efficacy Results {color="red_bg"}
---
**Always include this table — it is required for every trial entry.**
Rows cover **all** reported efficacy endpoints (PFS, OS, ORR, CR, PR, SD, CBR,
DOR, PFS2, EFS, iDFS, etc.; omit a row only if the trial genuinely did not
report that endpoint). Use "—" for unreported/immature data, not an empty cell.

Formatting rules (follow the BOLERO-2 page as the canonical example):
- Column headers: use the **actual arm names** (e.g., "Palbociclib + Fulvestrant"
  and "Placebo + Fulvestrant"), not generic labels.
- **Bold** the column header cells.
- Highlight each **primary endpoint row** with `color="yellow_bg"` on the `<tr>`;
  also bold the cell values in those rows.
- Include 95% CI for medians when reported (e.g., `6.9 mo (6.4–8.1)`).
- Include exact p-values; use `P<0.001` style.

```
<table header-row="true" header-column="true">
<tr>
<td>**Endpoint**</td><td>**[Study arm]**</td><td>**[Control arm]**</td><td>**HR (95% CI); P**</td>
</tr>
<tr color="yellow_bg">
<td>**Median PFS (mo)**</td><td>16.9 (15.2–20.9)</td><td>9.3 (7.5–10.3)</td><td>**0.63 (0.52–0.77); P<0.001**</td>
</tr>
<tr color="yellow_bg">
<td>**Median OS (mo)**</td><td>46.0 (42.5–51.8)</td><td>37.3 (33.4–42.2)</td><td>0.81 (0.65–1.00); P=0.048</td>
</tr>
<tr>
<td>ORR (%)</td><td>42.1% (38.6–45.7)</td><td>34.7% (31.2–38.3)</td><td>—</td>
</tr>
<tr>
<td>CR (%)</td><td>3.2%</td><td>1.1%</td><td>—</td>
</tr>
<tr>
<td>PR (%)</td><td>38.9%</td><td>33.6%</td><td>—</td>
</tr>
<tr>
<td>SD (%)</td><td>48.7%</td><td>48.0%</td><td>—</td>
</tr>
<tr>
<td>CBR (%)</td><td>68.1%</td><td>40.5%</td><td>—</td>
</tr>
<tr>
<td>Median DOR (mo)</td><td>—</td><td>—</td><td>—</td>
</tr>
</table>
```

(optional `<columns>` with OS / PFS sub-sections for Kaplan-Meier figures/notes)
### Safety {color="yellow_bg"}
---
- Key safety findings, grade >=3 AEs, discontinuation rates

# Discussion/Notes {color="yellow_bg"}
---
- Interpretation, clinical context, how this changes practice

# Reference {color="yellow_bg"}
---
- Plain-text citation(s): authors, journal, year
```

Use Notion markdown conventions seen in existing entries: `**bold**` for
labels, `<span color="...">` for highlights, `<details>` for collapsible
sections, `<table>`/`<columns>` blocks as shown above.

## Workflow

1. **Get inputs**: trial name (title) from `$ARGUMENTS` or ask the user if
   missing; confirm the reference attachment(s) are available (PDF, slide
   deck, or images already in the conversation/filesystem).
2. **Check for existing page**: search the database for the trial name using
   `mcp__claude_ai_Notion__notion-search` (query = trial name). If a page
   already exists in the Metastatic Cancer Database, **stop and inform the
   user** — show the existing page URL and ask whether to proceed anyway
   (e.g. to overwrite/update) or cancel. Do not create a duplicate silently.
3. **Extract source content**: read PDFs/images directly. If a `.pptx` can't
   be parsed directly, ask the user to export it to PDF or paste key slide
   screenshots instead — surface this as a limitation rather than failing
   silently.
4. **Map extracted data** to the schema fields above, matching existing
   multi-select option labels wherever possible.
5. **Write the properties** map following the concise conventions above.
6. **Compose the page body** following the detailed structure above.
7. **Create the page** with `mcp__claude_ai_Notion__notion-create-pages`:
   - `parent`: `{"type": "data_source_id", "data_source_id": "2a012797-0a62-81ff-b9bc-000b1334cb16"}`
   - `icon`: `"📊"`
   - `properties`: the mapped properties (title under `Key Trials/Med`)
   - `content`: the composed body (do not repeat the title in content)
8. **Report back**: share the new page URL, list any property values that
   were inferred/uncertain so the user can spot-check against the source,
   and remind them that the original file must be attached manually in
   Notion under Reference if they want it embedded — the Notion MCP tools
   available have no file-upload capability, so this skill cannot do that
   step automatically.
