# Clinical-trial database — data errors and rows needing a second look

Consolidated register covering **both** databases (Metastatic Cancer Database and
Early Stage Cancer Database), merged from the earlier `EFFICACY_SYMBOLS_REVIEW.md`
and everything found since. This file supersedes that one — it is the single
list to work from.

Every item below is either **a number that is provably wrong somewhere**, **a
statistic that is mislabelled**, or **a cell whose reading is ambiguous enough
that a verdict symbol could assert something false**. Nothing here is a matter of
taste.

---

## How to read the priority column

| Tier | Meaning | What it costs you if ignored |
|---|---|---|
| **P1** | Two conflicting values exist for the same statistic — one of them is wrong | The database states a falsehood today |
| **P2** | The statistic is internally impossible (CI does not contain its own point estimate) | Obvious error, undermines trust in the row |
| **P3** | The statistic is mislabelled (odds ratio called a hazard ratio, value in the wrong property) | Silently inverts interpretation |
| **P4** | Direction or arm order is ambiguous or inverted | A mechanical reading produces the opposite conclusion |
| **P5** | The statistic that would justify a symbol is missing from the cell | Row stays unmarked though the trial was positive |
| **P6** | Typo / truncation / stray character | Cosmetic, but several look like data |
| **P7** | Structural — one cell carries several populations, or a row sits in the wrong database | Blocks per-line marking |

---

## 1. P1 — Conflicting values (one of the two is wrong)

These are the highest-value fixes. In each case the same statistic appears twice
with different numbers, so the database currently asserts something untrue in at
least one place.

| # | Trial | Statistic | Value A | Value B | Note |
|---|---|---|---|---|---|
| 1 | **CALGB-SWOG 80405** | OS HR | `HR` property: **0.92 (0.78–1.09), p=0.34** | page body: **0.88 (0.77–1.01), P=0.08** | **Resolved in favour of B.** The FIRE-3 page's own cross-trial table independently gives "30.0 vs 29.0 months (HR 0.88; P=0.08)". The **0.92 / p=0.34 in the HR property is the outlier and is the value to correct.** |
| 2 | **MARIPOSA** | OS | property: **HR 0.74 (0.56–0.97), p=0.026** | body table: **HR 0.75 (0.61–0.92), p=0.005** | Different CI *and* different p. Both can't be the same analysis. |
| 3 | **EV-302** | median OS | property `mOS`: **33.6** | primary table: **31.5**; 2.5-yr update: **33.8** | Three values; **the property matches none of them.** |
| 4 | **IMpower 010** | ITT DFS HR | DFS cell: **0.81 (0.67–0.99)** | HR cell: **0.85 (0.71–1.01)** | The two disagree on **significance**, not just precision. HR cell left unmarked because of this. |
| 5 | **HIMALAYA** | STRIDE OS HR | `HR` cell: **0.78 (0.63–0.99)** | `mOS` cell + body: **0.78 (0.67–0.92)** | Same point estimate, two different CIs. |
| 6 | **MONALEESA-3** | 2L median PFS | property: **14.6** | body table: **14.9** | |
| 7 | **REACH-2** | PFS, control median | property: **1.5** | body: **1.9** | |
| 8 | **Saltz et al.** | ORR | property: **50% vs 28%** | body table: **39% vs 21%** | Both arms differ — not a rounding issue. |
| 9 | **RIGHT Choice** | ORR | property: **66.1% / 61.8%** | table: **74% / 68%**; figure: **65.2% / 60.0%** | **Three** different versions. CBR likewise 81.3/74.5 vs 80.4/72.7. |
| 10 | **RIGHT Choice** | TTF | body: **18.6 vs 9.1, HR 0.497 (0.363–0.680** *(bracket unclosed)* | figure: **18.6 vs 8.5, HR 0.45 (0.32–0.63)** | |
| 11 | **KN-224/240** | PFS p-value | HR property: **0.0022** | body: **0.022** | Matters — the prespecified boundary was 0.002, so A misses narrowly and B misses by 10×. |
| 12 | **IMpower133** | PFS p-value | results table: **p=0.002** | KM caption: **P=0.02** | Published value is **0.02**. ✅ either way. |
| 13 | **MONARCH-3** | PFS HR | figure caption: **0.64 (0.43–0.67)** | table + property: **0.535 / 0.54 (0.429–0.668)** | The caption is wrong on **both** estimate and CI — and its own CI excludes its own estimate (see §2). |
| 14 | **IMbrave 150** | ORR (mRECIST) | property: **35 vs 14** | body: **33.2% vs 13.3%** | ✅ either way (p<0.001), but should agree. |
| 15 | **DESTINY-Breast03** | OS HR paired with P=0.0037 | Discussion: **HR 0.64** | results table: **HR 0.73 (0.56–0.94)** | 0.64 is the Lancet 2023 2nd-interim figure; 0.73 is the Nat Med 2024 long-term figure. **The p-value belongs only to the former.** |
| 16 | **DESTINY-Breast03** | PFS HR | `HR` property: **0.28 (0.22–0.37)** | body table (BICR): **0.33 (0.26–0.43)** | Not an error — NEJM 2022 primary vs Lancet 2023 update — but **the cell doesn't say which cutoff**, so it reads as a contradiction. Add the cutoff label. |
| 17 | **INAVO-120** | OS | `mOS`/`HR` cells: interim **HR 0.64 (0.43–0.97), P=0.03, "not significant per interim boundary"** | row's own Key takeaway: *"2025 ASCO: OS benefit"* | The row is likely **out of date**. Marked ⚠️ off the cells; adding the final OS figures turns both lines ✅. |
| 18 | **SUNLIGHT** | effect of prior bevacizumab | subgroup toggle: "prior bev does **NOT** affect efficacy" | Key takeaway + Discussion: it matters a lot (**HR 0.40 vs 0.72**) | Internal contradiction within one page. |
| 19 | **PALOMA-3** | OS panel label | figure titled **"OS (ITT)"** | shows **20.2 vs 26.2, HR 1.14** | That is the endocrine-**resistant** subgroup, not ITT. Mislabelled panel. |

---

## 2. P2 — Statistically impossible values

A 95% CI must contain its own point estimate. These four do not, so at least one
number in each is mistyped.

| # | Trial | Cell reads | Why it can't be right |
|---|---|---|---|
| 20 | **EV-302** | OS **HR 0.47** with CI **(0.63–0.96)** | 0.47 lies outside 0.63–0.96. |
| 21 | **EV-302** (2.5-yr update) | **HR 0.61, 0.43–0.61** | Upper bound equals the point estimate. |
| 22 | **CM-8HW** | **PFS 0.21 (0.33–0.35)** | 0.21 lies outside 0.33–0.35. |
| 23 | **MONARCH-3** | figure caption **HR 0.64 (0.43–0.67)** | 0.64 is inside 0.43–0.67, but the table gives 0.535 (0.429–0.668) — the caption is a garbled copy of it. |
| 24 | **ReTrITA** | monotherapy medians vs CIs: R mOS **5.0 (9.0–13.4)**, T mPFS **3.3 (4.0–4.8)**, R mPFS **3.2 (3.8–4.9)** | **Three in a row** where the median sits below the entire CI — the CI column looks **shifted by one row**. Fix as a block, not one at a time. |

---

## 3. P3 — Mislabelled statistics

The label says one thing, the number is another. This is the class most likely to
mislead a reader who trusts the column header.

| # | Trial | Cell says | Actually is | Consequence |
|---|---|---|---|---|
| 25 | **P025** | "ORR **HR** 1.78 (1.32–2.40)" | **Odds ratio** | A hazard ratio of 1.78 would mean letrozole did *worse*; as an OR it means letrozole did **better**. Exactly inverted. |
| 26 | **NIAGARA** | "pCR **HR** 1.30 (1.09–1.56)" | **Odds ratio** | Same error class. >1 is favourable here. Marked ✅. |
| 27 | **PARADIGM** | `DCR` property holds **74.9% vs 67.3%** | The body identifies this as **ORR (Overall)** | Value is in the **wrong property**. DCR is currently unpopulated and ORR is wrong. |
| 28 | **MARIPOSA-2** | `HR` property carries only the **two PFS** comparisons | Both **OS** rows exist, but only in the body | The property understates what the trial reported. |
| 29 | **SOFT** | `HR` property holds the **12-year** update (0.82/0.78/0.83) | Body table holds the **8-year** analysis (0.76/0.67/…) | Not wrong, but neither says which — reads as a discrepancy. |
| 30 | **PARADIGM** | — | PFS right-sided **HR 1.43 (1.03–1.97)** — bevacizumab significantly **better** — exists only in the body | A clinically important negative result is missing from the properties. |

---

## 4. P4 — Direction traps and arm-order problems

Rows where reading the numbers left-to-right gives the **wrong answer**.

| # | Trial | The trap | Status |
|---|---|---|---|
| 31 | **INT-0116** | OS HR **1.32** (1.10–1.60; P=.0046) with medians 36 vs 27 favouring chemoradiation. **The HR is expressed for the surgery-only arm**, so HR>1 means the study arm won. | **Left fully unmarked.** A mechanical pass would have put ❌ on a positive trial. Rewrite the cell to state the direction. |
| 32 | **CALGB-SWOG 80405** | `ORR` reads "55.2% vs 59.6%" while `Drug/Control` is "Cetuximab vs bevacizumab" and the body gives cetuximab **59.6%** — **the arms in the ORR cell are reversed** relative to every other cell in the row. Independently confirmed by the FIRE-3 page ("59.6% vs 55.2%, P=0.13", cetuximab first). | ORR left unmarked. |
| 33 | **KRISTINE** | Ordering is experimental-first, so pCR 44.4% vs 55.7% and EFS HR 2.61 mean the **experimental** arm did worse. | Marked ❌. **Please confirm the arm order is as I read it.** |
| 34 | **RAPIDO** | "3yr DrTF 23.7% vs 30.4%" is a **failure** rate — lower is better. | Marked ✅ (correct), but the cell reads backwards at a glance. |
| 35 | **CASPIAN (PFS)** | HR 0.78 (0.65–0.94) favours durvalumab; medians read 5.1 vs 5.4 and favour control. | Marked ✅ off the HR. Row looks self-contradictory. |
| 36 | **Gem-carbo** | PFS medians (5.8 vs 4.2) favour arm 1; HR **1.04** points the other way. | **Left unmarked — one of the two is wrong.** |
| 37 | **CAIRO5** | Could not determine whether the "9.0 vs 10.6" ordering matches the HR direction. | **Left unmarked.** |
| 38 | **PARADIGM (PFS, left-sided)** | Medians favour panitumumab (13.1 vs 11.9) but HR is exactly **1.00** (0.83–1.20). | **Left unmarked** — flagged rather than guessed. |
| 39 | **ADRIATIC** | ORR **30.3% vs 32.0%** favours the *control* arm, on a row that is otherwise positive. | Left unmarked (no test). Worth a note in the row. |
| 40 | **IMpower133** | ORR **60.2 vs 64.4** — control responded more often, next to two ✅s on PFS and OS. | Left unmarked (no test). Same shape as #39. |

---

## 5. P5 — Missing statistics that block a verdict

These trials were positive in publication but the cell carries no test, so the
symbol pass had to leave them bare. Adding the statistic makes each markable.

| # | Trial(s) | What's missing |
|---|---|---|
| 41 | **CM-77T, CM-816, KN-671, KN-905/EV-303, MATTERHORN, FLOT4, RAPIDO, PICC** | pCR reported with **no p-value**; several were significant in publication. |
| 42 | **BREAKWATER** | ORR is the **primary endpoint**; the cell has no p-value, though the body gives **OR 2.44, P<0.001**. Marked ✅ off the body — move the statistic into the cell. |
| 43 | **CASPIAN** | `ORR` gives only the durvalumab arm ("79% unconfirmed; 68% confirmed") with **no comparator**. Marked ✅ from the underlying comparison (OR 1.64, 1.11–2.44 vs 70%); the cell should carry both arms. |
| 44 | **MAINTAIN** | ORR **P=0.51** and CBR **P=0.06** existed only in the body. Both now marked ⚠️ — worth promoting to the cells. |
| 45 | **FALCON** | Only the ITT line has statistics; the non-visceral and visceral subgroups have none in the row, so only ITT is marked. |
| 46 | **RASolute 302 / STELLAR-303 / TROPION-Breast02** | ORR marked only where a formal OR/CI on the *difference* exists; elsewhere left bare. |

---

## 6. P6 — Typos, fragments, stray characters

| # | Trial | Cell | Reads | Should read |
|---|---|---|---|---|
| 47 | **Gem-cis** | `PFS` | "7.7 vs **8,3**" | 8.3 (comma for decimal point) |
| 48 | **RECOURSE** | DCR | "44**$**" | 44% |
| 49 | **ReTrITA** | property | "11.5**vs**. 8.5" | missing space |
| 50 | **KN-224/240** | body | "p**Sembro**" | stray character |
| 51 | **SUNLIGHT** | `mOS` line 2 | "Prior bev 9" | unfinished fragment |
| 52 | **MARIPOSA-2** | `HR` line 2 | "…(0.35–0.56) **for Ami+Laz+ChT vs ChT**" | arm label repeated |
| 53 | **RIGHT Choice** | body TTF | "HR 0.497 (0.363–0.680" | unclosed bracket (see #10) |
| 54 | **KN-355** | body | "Prespecified statistical criterion of alpha=0·00411" stated once **as if global** | It applies only to the CPS ≥10 PFS test; OS used ~0.0193. |

---

## 7. P7 — Structural problems

### 7a. One row is in the wrong database

| # | Trial | Problem |
|---|---|---|
| 55 | **SOFT** | Its own *Patient population* field says **"Adjuvant setting"**, yet the row sits in the **Metastatic** database. |

### 7b. Cells packing several populations onto one line

A single symbol would misreport these. Splitting onto separate `<br>` lines (as
MONALEESA-3 now is) lets each population carry its own verdict.

| # | Trial / cell | Why one symbol can't work |
|---|---|---|
| 56 | **CM-8HW (PFS)** | "24M 72% vs 55% vs 14%" packs **both dual primary comparisons** with **opposite** verdicts: nivo-ipi vs chemo was positive (HR 0.21, p<0.0001 → ✅), but nivo-ipi vs nivo monotherapy **missed its boundary** (p=0.0413 vs 0.0383), so dual-IO superiority could not be declared. **Left unmarked.** |
| 57 | **CAPItello-291 (OS)** | "29.4 vs 28.6 (overall); 28.5 vs 30.4 (AKT-alt)" on one line — overall is ❌, AKT-altered is ⚠️. |
| 58 | **SOFT**, **ARTIST 2** | Three-arm percentages, not a two-arm median. |
| 59 | **EMERALD (OS)**, **HIMALAYA (PFS)**, **KN-048**, **MARIPOSA-2 (OS)**, **GERCOR**, **PARADIGM (PFS)** | Multiple populations per line. |
| 60 | **SUNLIGHT mOS line 2**, **ReTrITA monotherapy lines** | Descriptive, no test — left unmarked. |

---

## 8. Rows where the verdict is a judgment call — please confirm

These are **not** data errors. They are rows where the number and the trial's own
conclusion point different ways, and I chose the trial's conclusion. Each one is
reversible in a single edit.

| Trial | Cell | Applied | Why it's arguable |
|---|---|---|---|
| **KN-177** | OS | ⚠️ | HR 0.73 (0.53–0.99) — the CI **excludes** 1, which normally earns ✅. But the body says OS "did not reach statistical significance and was not formally re-tested" at the 2021 final analysis. This is the **mirror image of FLAURA**: there a CI *touching* 1 earned ✅ because the trial met its boundary; here a CI *clearing* 1 gets ⚠️ because it did not. |
| **KN-355** | PFS, CPS ≥1 | ⚠️ | The page **bolds** "0.75 (0.62–0.91), p=0.0014" as if significant. The Lancet hierarchy set alpha at 0.00111 for that population, so it missed. The row's own Key takeaway ("improves BOTH PFS and OS in **CPS ≥10**") agrees with ⚠️. |
| **STELLAR-303** | PFS | ⚠️ | HR 0.68 (0.59–0.79) looks strongly positive; the results table itself says *"hierarchical testing: superiority not formally claimable yet"*. |
| **TRIPLETE** | OS | ✅ | HR 0.79 (0.63–0.99), p=0.049 — but this is a later OS update on a trial whose **primary endpoint (ORR) failed**, and your own Key takeaway asks *"Final OS positive???"*. Treat as provisional. |
| **MORPHEUS-Liver** | PFS, OS | ✅ ✅ | Both CIs exclude 1, but this is a randomised **phase 1b/2, N=59**, whose control arm badly underperformed IMbrave150 (ORR 11% vs 30%). The checks reflect the CIs, not a confirmatory result. |
| **ReTrITA** | PFS, OS | ✅ ✅ | **Retrospective** real-world study (Phase = "Retro"). Checks come from adjusted real-world HRs, not randomisation. |
| **ACOSOG Z1031** | whole row | **left blank** | 3-arm AI-vs-AI phase II **selection** design with **no control**. PEPI-0 P=.9 means the three AIs didn't differ — not that neoadjuvant AI failed. A ❌ would state the opposite of the trial's conclusion. |
| **MONALEESA-3** | 1L OS line | ✅ | CI **0.48–1.02** *crosses* 1 rather than resting on it, so unlike the other borderline rows this line isn't significant on its own terms. Applied ✅ per your rule (prespecified subgroup, significant ITT, same direction as 2L) — but it is the one cell where ✅ asserts something the subgroup statistic alone doesn't support. Say the word and I'll revert this line only. |
| **EMILIA** | OS | ✅ ✅ | Both the 2nd interim (HR 0.68, P<0.001) and the final analysis (HR 0.75, "descriptive") are green. The final is descriptive only because alpha was spent, not because the result is in doubt (CI 0.64–0.88 still excludes 1). ⚠️ there would imply EMILIA's OS benefit is uncertain, which is wrong. |

---

## 9. One rule conflict — I need your decision

Two rows have the **same shape** and currently carry **different symbols**:

- **FIRE-3** — ORR was the primary endpoint and **failed** (62% vs 58%, p=0.18).
  The drug arm was numerically **better**. Marked **❌**.
- **RCT by HORG** — OS was the primary endpoint and **failed** (21.5 vs 19.5 mo,
  p=0.337). The drug arm was numerically **better** on every endpoint.
  Marked **⚠️**.

Pick one and I'll make both match:

- **(a)** A failed primary endpoint is ❌ regardless of direction → flip **HORG to ❌**.
- **(b)** ❌ only when the control arm actually did better → flip **FIRE-3's ORR to ⚠️**.

Everything else in the pass follows **(b)**. I left HORG at ⚠️ because a red ✗
next to "21.5 vs 19.5 months" reads as *FOLFOXIRI did worse*, which is false.

---

## 10. Trials that missed their own prespecified boundary

Not errors — but each looks significant under a naive p<0.05 read and is **not**.
Recorded here so nobody "corrects" them back to ✅.

| Trial | Statistic | Boundary it missed |
|---|---|---|
| **KN-224/240** | OS p=0.0238; PFS p=0.0022 | boundaries 0.0174 and 0.002 — both missed |
| **LEAP-002** | OS p=0.023 | boundary 0.0185 |
| **KN-355** | PFS/OS significant in **CPS ≥10 only** | CPS ≥1 and ITT not formally met |
| **EMERALD** | ESR1-mut OS **HR 0.59 (0.36–0.96), p=.03** | Haybittle-Peto interim alpha **0.0001**. The clearest counterexample to "CI excludes 1 → ✅". |
| **INAVO-120** | interim OS HR 0.64 (0.43–0.97), P=0.03 | flagged "not significant per interim boundary" — see #17 |
| **KN-177** | OS | never formally re-tested — see §8 |
| **STELLAR-303** | PFS | hierarchical testing not yet claimable — see §8 |
| **CM-8HW** | nivo-ipi vs nivo-mono p=0.0413 | boundary 0.0383 — see #56 |

### The borderline-CI rule, as you set it

A CI bound sitting **on** (or a hundredth past) 1.00 does **not** make a result
negative when the trial met its own significance level and the effect is
clinically meaningful. Applied to:

| Row | Statistic |
|---|---|
| **FLAURA** | OS HR 0.80 (0.64–**1.00**), p=0.046 vs prespecified alpha 0.0495 — boundary met → ✅ |
| **MONALEESA-3** | 1L HR 0.70 (0.48–**1.02**); 2L HR 0.73 (0.53–**1.00**), under a significant ITT (HR 0.72, P=0.00455) → ✅ |

`SKILL.md` has been rewritten to match, so future `/add-trial` entries follow it
automatically. **⚠️ now means only** "failed its own prespecified test, was never
formally tested, or is immature" — it no longer means "CI touches 1".

---

## 11. Primary endpoints that genuinely failed (marked ❌ — sanity-check)

| Trial | Statistic |
|---|---|
| **FIRE-3** | primary ORR failed (OR 1.18, p=0.18) despite the well-known OS benefit — ORR ❌ and OS ✅ on the same row |
| **TRIPLETE** | primary ORR failed (OR 0.87, P=.526) |
| **AVANT** | bevacizumab arms were **worse**: OS HR 1.27 (1.03–1.57), p=0.02 |
| **CAIRO2** | PFS HR 1.22 (1.04–1.43), p=0.01 — significantly worse |
| **PARSIFAL** | PFS HR 1.13, P=.32 |
| **KRISTINE** | see #33 |
| **APHINITY (node-negative)** | iDFS HR 1.01 (0.72–1.42) |
| **HERA** | 2-yr vs 1-yr trastuzumab DFS HR 1.02 |

---

## 12. Rows deliberately left unmarked (confirmed — no action needed)

### 12a. Single-arm trials — no comparator, so no verdict exists
ABBV-400 · ByLieve · CM-040 · CM-275 · DESTINY PanTumor-02 · DESTINY-Breast12 ·
DESTINY-CRC01 · HERACLES-A · KCSG-LU15-09 · MOUNTAINEER · MyPathway · PYNNACLE ·
TriComB · NSABP-B27 (Real-world) · Cercek et al · Ludford et al · NICHE-2

### 12b. Rows with no efficacy data at all
ALEX · ASPECT · Beamion-Lung 01 · CodeBreak 301 · KANDLELIT-012 · KN-016 ·
KN-042 · KN-189 · KN-407 · RMC-6236 · SOHO-01 · AZUR-2 · NEOADAURA ·
"Template for Early Cancer" (template row, not a trial)

### 12c. Not a treatment comparison
- **CTNeoBC** — pooled analysis of pCR-vs-no-pCR *prognosis*; the HRs describe
  outcomes by response, not a drug effect.
- **TransNEOS** — the OR describes Recurrence Score as a *predictor* of clinical
  response, not a treatment effect.
- **TRYPHAENA** — primary endpoint was cardiac safety; the three-arm pCR figures
  are descriptive.
- **DeLLphi-305** — the OS figure is a cross-trial comparison against IMP133.

### 12d. Non-inferiority designs — marked **↔**, not ✅/❌
"Not worse" was the question, so both ✅ and ❌ would misreport them.

| Trial | Marked **↔** | Other endpoints on the same row |
|---|---|---|
| ASPECCT | OS (NI p=0.0007), PFS | — |
| Gem-cis | OS, PFS | — |
| RATIONALE-301 | OS (NI p=0.04) | PFS ❌ (HR 1.11, 2.1 vs 3.4) |
| REFLECT | OS (HR 0.92, NI met) | PFS ✅ (HR 0.66, P<0.001) |
| PROSPECT | DFS (NI P=0.005), OS, LRR | — |
| STELLAR | DFS (NI p<0.001) | OS ✅ (HR 0.67, p=0.033); MFS ⚠️; pCR ✅ (p=0.002) |
| HIMALAYA | OS, durvalumab-mono arm only (HR 0.86, 0.73–1.03 vs NI margin 1.08) | STRIDE OS ✅ (HR 0.78, p=0.0037); **both** PFS lines ❌ |

REFLECT and STELLAR are the interesting ones — non-inferior on the primary
endpoint but genuinely *superior* on a secondary, so the row carries **↔** and ✅
side by side. HIMALAYA is the only row where **↔**, ✅ and ❌ all appear together;
a per-trial verdict would have flattened all of it.

---

## 13. Suggested order of work

1. **§1 (#1–#19)** — every one of these means a wrong number is live in the
   database right now. #1 (CALGB OS HR) is already resolved and just needs the
   edit; #3 (EV-302 mOS) and #9 (RIGHT Choice ORR) are the messiest.
2. **§2 (#20–#24)** — five minutes each, and #24 (ReTrITA) is likely one
   off-by-one-row paste that fixes three lines at once.
3. **§3 (#25–#30)** — #25 (P025) is the one that actively inverts meaning.
4. **§9** — the one decision only you can make; unblocks two rows.
5. **§5 (#41–#46)** — pure upside: each added p-value converts an unmarked cell
   into a marked one.
6. Everything else is cosmetic or already correctly handled.

---

## Legend used across both databases

| Symbol | Meaning |
|---|---|
| ✅ | Statistically significant benefit — endpoint met (p below the prespecified boundary, or HR 95% CI excluding 1) |
| ⚠️ | Failed its own prespecified test, was never formally tested, or immature. **Not** "CI touches 1" |
| ❌ | No benefit, endpoint not met, or the control arm did better |
| **↔** | **Non-inferiority met** — powered to show "not worse", so an HR near 1 is a success. Applied per endpoint |
| *(no symbol)* | Deliberately unmarked — see §12 |

**Marking scope.** PFS / OS / DFS / EFS are marked from the trial's own HR and
p-value. Response endpoints (ORR, DCR/CBR, pCR) are marked **only** where a
p-value or confidence interval actually exists — in the cell or in the page body.
A response rate reported with no test is left unmarked rather than guessed at.
Symbols are applied **per result line**, never per trial.

---

# Part 2 — the early-stage database (both databases now complete)

The Early Stage Cancer Database has been worked end to end: **56 rows, 45
marked, 11 deliberately unmarked**. Together with the 103 metastatic rows,
**148 rows now carry per-endpoint symbols**.

Everything below is new. Item numbers continue from §1–§7 above.

## 14. Two corrections to the register above

| # | What changes | Why |
|---|---|---|
| **61** | **#26 (NIAGARA) — the verdict was wrong.** The OR-mislabelled-as-HR finding stands, but the row is now **⚠️, not ✅**. | pCR was a **dual primary** endpoint and the page says outright: *"pCR rate did **NOT** meet the pre-specified significance threshold (p<0.001)"* — the reported p was 0.004. The row's own Key takeaway reads "EFS, OS +, **pCR −**". |
| **62** | **#4 (IMpower 010) is not an error — downgrade it.** | The DFS cell holds the **2021 interim** analysis (ITT HR 0.81); the HR cell holds the **2024 five-year update** (ITT HR 0.85). Two data cutoffs, not a contradiction. Same class as #16. **Fix = label the cutoffs**, not reconcile the numbers. |

Two register items can also be **closed**:

- **#33 (KRISTINE arm order)** — confirmed. `Drug/Control` is "T-DM1+P vs TCHP",
  experimental-first, and pCR 44.4% vs 55.7% (diff −11.3%, p=0.016) means the
  experimental arm did worse. The reading was right.
- **#1 (CALGB OS HR)** — unchanged, still the highest-value single fix.

## 15. New P1 — conflicting values

| # | Trial | Statistic | Value A | Value B |
|---|---|---|---|---|
| **63** | **MAGIC** | **OS and PFS hazard ratios are SWAPPED in the `HR` property.** | property: "PFS 0.66 (0.53–0.81, p<0.001)" and "OS 0.75 (0.60–0.93, p=0.009)" | **both** body tables: 5yr **OS** (primary) HR **0.66**; 5yr **PFS** HR **0.75**. The property has the labels the wrong way round. |
| 64 | **CM-816** | EFS | property + 5-yr table: **HR 0.68 (0.51–0.91)** | primary table: **0.63 (97.38% CI 0.43–0.91)**; figure caption: **0.66 (0.49–0.90)**, with mEFS "43.8 vs 18.4" against the property's "31.6 vs 20.8" |
| 65 | **CM-816** | OS HR | property + figure: **0.69 (0.49–0.97)** | OS table: **0.72 (0.523–0.998)** |
| 66 | **CM-816** | p-value attachment | P=0.005 sits on HR 0.68 in the property | it belongs to the **primary** analysis (HR 0.63) — same shape as #15 |
| 67 | **ARTIST** | DFS p-value | property + HR cell: **0.0922** | results table: **0.0862** |
| 68 | **ARTIST** | DFS timepoint | property: "**5yr** DFS 78.2% vs 74.2%" | the primary table labels the **same numbers** "**3yr** DFS" |
| 69 | **ARTIST** | LN+ subgroup | table: **77.5% vs 72.3%, p=0.0365** | subgroup detail: **76% vs 72%, P=0.04** |
| 70 | **KN-671** | EFS HR | property + figure: **0.58 (0.46–0.72)** | primary table: **0.59 (0.48–0.72)**. The table also calls 3-yr EFS "3yr **RFS**". |
| 71 | **MATTERHORN** | EFS timepoint | property: "**2yr** EFS 67% vs 59%" | table: "**1yr** EFS 67.4% vs 58.5%" |
| 72 | **CM-77T** | EFS | property: "**1yr** EFS 73% vs 59%" | table: "**18-M** EFS 70.2% vs 50.0%" — the property's numbers appear **nowhere** in the body |
| 73 | **JACCRO GC-07** | 5yr RFS | property: **59.8% vs 50.6%** | the secondary table's "5yr RFS" row **repeats the 3yr percentages** (67.7% vs 57.4%) |
| 74 | **FNCLCC-FFCD** | R0 rate | Patient population: **PF 84%** | both body tables: **87%** |
| 75 | **FNCLCC-FFCD** | grade ≥3 neutropenia | property: **22%** | safety section: **20.2%** |
| 76 | **CLASSIC** | completion | `Completion (%)`: **32%** | body: "Only **67%** of patients completed 8 cycles" |
| 77 | **SAMIT** | TS-1 3yr DFS | property: **58.1%** | table: **58.2%** |

## 16. New P2/P3 — impossible or mislabelled

| # | Trial | Problem |
|---|---|---|
| 78 | **AMBASSADOR** | Body table: "DFS (CPS <10)" HR reads "**0.53–0.95)**" — the point estimate and opening bracket are missing entirely. |
| 79 | **AMBASSADOR** | CPS ≥10 DFS is **not** significant (0.81, 0.61–1.08) while CPS <10 **is** — the page already flags this with a "??" callout, but it is worth confirming against the publication. |
| 80 | **DESTINY-Breast05** | The population callout is headed "**T-DXd \| T-DM1**" but its rows (dual-HER2 70/20, N+ 80/45, inoperable 50/20) actually compare **DB-05 with KATHERINE**. As headed, it reads as a severe baseline imbalance between the two arms. |
| 81 | **DESTINY-Breast05** | Same callout gives 70/80/50 where the body text gives **79% / 80.7% / 52.7%**. |
| 82 | **APHINITY** | `HR` cell: "8-yr OS (**IIT**)" — typo for ITT. |
| 83 | **HERA** | `HR` cell labels OS "**(11-yr)**"; the property and table both report **12-yr** OS. |
| 84 | **MOSAIC** | `HR` cell: "OS **HR HR** 0.90" — duplicated. |
| 85 | **FLOT4** | `HR` cell: "DFS 0.75 **0.62–0.91**, p=0.0036)" — missing opening bracket. |
| 86 | **BCIRG-006** | The trastuzumab arm is labelled **three different ways in one row**: "AC-T+T", "AC-T+H", "AC-H+T". |
| 87 | **P024** | The `pCR (%)` property holds **ORR**, not pCR — a workaround for the early-stage schema having no ORR field. It *is* labelled "Primary endpoint ORR", so this is a schema gap rather than an error. |
| 88 | **ARTIST 2** | SOX vs S-1 HR **0.693 (0.409–0.987)** — the CI is markedly asymmetric on the log scale, which is unusual for a Cox hazard ratio. Worth checking against Ann Oncol 2021. |
| 89 | **ARTIST 2** | `DFS` lists arms S-1 / SOX / SOXRT; `Drug/Control` lists SOX / SOX-RT / S-1. Different order in the same row. |
| 90 | **ARTIST**, **ARTIST 2**, **CM-274**, **MATTERHORN** | Table header typos: "HR (95% CI, p **valua**)" / "p **valu**". |
| 91 | **ARTIST** | Body: "Distant recurrence … p = **5568**" — missing the leading "0.". |
| 92 | **KN-355** *(metastatic, found while cross-checking)* | "Prespecified statistical criterion of alpha=0·00411" is stated once as if global; it applies only to the CPS ≥10 PFS test. |

## 17. New P4/P7 — direction, structure, and completeness

| # | Trial | Problem |
|---|---|---|
| 93 | **ARTIST (OS)** | 5yr OS **75% vs 73%** favours the study arm, but **HR 1.13** favours control. Direction conflict. Null either way (p=0.5272), so the ⚠️ stands, but the row contradicts itself. |
| 94 | **KRISTINE (IDFS)** | 3yr IDFS **93.0% vs 92.0%** favours T-DM1+P, but **HR 1.11** favours TCH+P. Same conflict. |
| 95 | **AVANT** | `HR` cell had a **stray `<br>`** splitting "HR 1.27" from "(1.03–1.57; p=0.02)". **Repaired** into four clean lines while marking. |
| 96 | **SAMIT** | `HR` cell has **two** stray `<br>` tags splitting statistics mid-value. Left verbatim; the orphan fragments carry no symbol. |
| 97 | **DESTINY-Breast11** | The **T-DXd-alone arm was INFERIOR** (ΔpCR −13.2%, P=0.001; closed early by the IDMC) — that appears **only in the body**. The properties show only the winning comparison. |
| 98 | **NeoSphere** | **Group D** (pertuzumab + docetaxel, no trastuzumab) was significantly **worse** than control — PFS HR 2.05 (1.07–3.93), DFS HR 2.16 (1.08–4.32) — body only. |
| 99 | **PARADIGM** *(metastatic)* + **NSABP B-27** | B-27's DFS and OS properties read "NA (no exact number)" although the body carries HR ~0.94, P=NS. |
| 100 | **PRODIGE 23** | The Key takeaway claims TNT improved "DFS, MFS, **and OS**", but the only OS statistic on the page is **HR 0.65, p=0.0773** (not significant), and the 7-yr figures (82% vs 72%) carry **no HR or p at all**. |
| 101 | **KATHERINE** | `HR` line 3 packs IHC 3+ (0.47, positive) and IHC 2+ (0.84, not) onto one line — **left unmarked**, needs splitting. |
| 102 | **IMpower 010** | Both `HR` lines pack **four** and **two** populations with different verdicts — **left unmarked**, needs splitting. |
| 103 | **AVANT**, **NO16968** | Page bodies are **completely blank** (properties only). With FALCON, that's three. |
| 104 | **SUNLIGHT** *(metastatic)* | *(already #18)* — internal contradiction on prior bevacizumab. |

## 18. Three more rows deliberately left unmarked

Added to §12. All three are **randomised trials without a comparative test**,
so any symbol would assert something the design cannot support.

| Trial | Why |
|---|---|
| **GEICAM/2006-03** | Randomised **phase II, explicitly not designed to compare the arms** (Simon two-stage on the endocrine arm only; the primary result is reported as "P=0.075 *(exploratory)*"). The only markable property is pCR — **1 patient vs 0**. |
| **PICC** | Randomised **phase 2, non-comparative**; both arms had 1-yr DFS and OS of **100% with no events**; pCR carries no test. |
| **ACOSOG Z1031** | *(already in §8)* — 3-arm selection design with no control. |

## 19. One more decision for you

**NSABP B-18 and TRAIN-2** are the same shape and I marked both **⚠️**:

- **B-18** — neoadjuvant vs adjuvant AC. Dual primary OS and DFS, both null
  (RR 1.02, P=.80; RR 0.95, P=.50). The field reads this as **equivalence**.
- **TRAIN-2** — anthracycline vs anthracycline-free. pCR 67% vs 68%, P=.95.
  Read as **"anthracyclines add nothing"**.

Neither trial prespecified a **non-inferiority margin**, so **↔** would claim
more than the design supports — that is why both are ⚠️. But ⚠️ reads as
"inconclusive", when the clinical message in both cases is closer to "these are
equivalent, pick the less toxic one".

**If you'd rather these two carry ↔, say so and I'll change both.** They are the
only rows in either database where a failed superiority test is treated as a
practice-defining equivalence result.
