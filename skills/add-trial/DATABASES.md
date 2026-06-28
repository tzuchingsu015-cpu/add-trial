# Trial Database Routing

There are **two** separate Notion databases for clinical trials. Route each trial
to the correct one based on its **disease setting**, and use that database's schema.

## 1. Early Stage Cancer Database

- **When:** adjuvant, neoadjuvant, or peri-operative (early-stage / curative-intent) trials.
- **Data source id (parent for new pages):** `2a312797-0a62-81c7-82ef-000b4de44d4b`
- **Title property:** `Key Trials/Med`
- **Distinctive schema:**
  - `Timing` (select): Peri-OP, Neoadjuvant, Adjuvant
  - `Treatment` (multi-select): ADC, ICI, RT, TKI, ChT, **Anti-HER2**
  - `Biomarker` (multi-select): HER2, ER/PR (HR), PD-L1, BRCA1/2, PIK3CA, ESR1, EGFR, ALK, MSI-H / dMMR, ctDNA
  - `Cancer type` (**single** select): Other, Endometrial CA, Cerical CA, Ovary, Sarcoma, Skin, CRC, GC, Esophagus, UC, Pancreas, BTC, HCC, Breast, Lung, NPC, HEENT
  - `Phase` (multi-select): Meta, Ongoing, I, II, III, Retro
  - Text/number: `Number`, `DFS ` (note trailing space), `PFS`, `OS`, `pCR (%)`,
    `Completion (%)`, `HR (95% CI)`, `Drug/Control`, `Patient population`,
    `>= Gr. 3 TRAE`, `Key takeaway`, `Year`

## 2. Metastatic Cancer Database

- **When:** metastatic / advanced-disease trials.
- **Data source id (parent for new pages):** `2a012797-0a62-81ff-b9bc-000b1334cb16`
- **Title property:** `Key Trials/Med`
- **Distinctive schema:**
  - `Line` (multi-select): 1, 2, 3
  - `Phase` (multi-select): Retro, Ongoing, I, II, III
  - `Treatments` (multi-select): NSAI, Anti-EGFR, SERD, CDK4/6i, Endocrine, RT,
    BsAb, Others, ADC, TKI, Anti-VEGF, ICI, ChT (no dedicated Anti-HER2 option — use Others)
  - `Cancer type` (multi-select), `Biomarker` (multi-select)
  - Text/number: `Year`, `Drug/Control`, `Patient population`, `mOS (month)`,
    `PFS (month)`, `HR (95% CI)`, `ORR (%)`, `CR (%)`, `PR (%)`, `SD (%)`,
    `DCR (%)`, `>= Gr. 3 TRAE`, `Key takeaway`

## Routing rule

1. Determine the setting from the source: adjuvant / neoadjuvant / peri-op → **Early Stage DB**;
   metastatic / advanced → **Metastatic DB**.
2. If the source describes both (e.g. a combined early + advanced program), ask the user.
3. Always check the target database for an existing page before creating (avoid duplicates).
4. Map the trial to **that database's** fields — do not force metastatic-only fields
   (Line, PFS/OS medians, ORR) onto an early-stage trial, or vice versa.

> Background: BCIRG-006 (adjuvant HER2+ early breast cancer) was initially added to the
> Metastatic DB by mistake; its fields didn't fit. This doc exists to prevent a repeat.
