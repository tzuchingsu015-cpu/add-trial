# Efficacy symbol pass — items needing your review

Legend applied across both databases:

| Symbol | Meaning |
|---|---|
| ✅ | Statistically significant benefit — endpoint met (p below the prespecified boundary, or HR 95% CI excluding 1) |
| ⚠️ | Failed its own prespecified test, was never formally tested, or immature. (Does **not** mean "CI touches 1" — see §3a) |
| ❌ | No benefit, endpoint not met, or the control arm did better |
| **↔** | **Non-inferiority met** — the endpoint was powered to show "not worse", so a hazard ratio near 1 is a success. Applied per endpoint, not per trial |
| *(no symbol)* | Deliberately left unmarked — see below |

**Marking scope.** PFS / OS / DFS / EFS are marked from the trial's own HR and
p-value. Response endpoints (ORR, DCR/CBR, pCR) are marked **only** where a
p-value or confidence interval actually exists for that endpoint — either in the
cell itself or in the page body. Where a response rate is reported without any
test, it is left unmarked rather than guessed at.

---

## 1. Rows deliberately left unmarked

### 1a. Single-arm trials — no comparator, so no verdict is possible
ABBV-400 · ByLieve · CM-040 · CM-275 · DESTINY PanTumor-02 · DESTINY-Breast12 ·
DESTINY-CRC01 · HERACLES-A · KCSG-LU15-09 · MOUNTAINEER · MyPathway · PYNNACLE ·
TriComB · NSABP-B27 (Real-world) · Cercek et al · Ludford et al · NICHE-2

A symbol here would imply a comparison that was never made. **Confirmed
decision: these stay blank.**

### 1b. Non-inferiority designs — now marked **↔** (RESOLVED, applied)
These trials asked "is it *not worse*", not "is it better", so ✅/❌ would both
misreport them. All six are done:

| Trial | Endpoint marked **↔** | Other endpoints |
|---|---|---|
| ASPECCT | OS (NI p=0.0007), PFS | — |
| Gem-cis | OS, PFS | — |
| RATIONALE-301 | OS (NI p=0.04) | PFS ❌ (HR 1.11, median 2.1 vs 3.4) |
| REFLECT | OS (HR 0.92, NI met) | PFS ✅ (HR 0.66, P<0.001) |
| PROSPECT | DFS (NI P=0.005), OS, LRR | — |
| STELLAR | DFS (NI p<0.001) | OS ✅ (HR 0.67, p=0.033); MFS ⚠️; pCR ✅ (p=0.002) |
| HIMALAYA | OS, durvalumab-mono arm only (HR 0.86, CI 0.73–1.03 vs NI margin 1.08) | STRIDE OS ✅ (HR 0.78, p=0.0037); both PFS lines ❌ |

Note REFLECT and STELLAR are the interesting ones: non-inferior on the primary
endpoint but genuinely *superior* on a secondary, so the row now carries **↔**
and ✅ side by side — which is the correct reading of both trials.

HIMALAYA is the seventh, found later in the pass, and is the only row where **↔**
and ✅ and ❌ all appear together: the STRIDE arm beat sorafenib on OS (✅), the
durvalumab-monotherapy arm only had to prove non-inferiority and did (**↔**), and
*neither* arm improved PFS — sorafenib's median was numerically longer in both
comparisons (❌ ❌). A per-trial verdict would have flattened all of that.

### 1c. Rows with no efficacy data at all
ALEX · ASPECT · Beamion-Lung 01 · CodeBreak 301 · KANDLELIT-012 · KN-016 ·
KN-042 · KN-189 · KN-407 · RMC-6236 · SOHO-01 · AZUR-2 · NEOADAURA ·
"Template for Early Cancer" (template row, not a trial)

### 1d. Not a treatment comparison
- **CTNeoBC** — pooled analysis of pCR-vs-no-pCR *prognosis*, not a randomised
  comparison. The HRs describe patient outcomes by response, not a drug effect.
- **TransNEOS** — the OR describes Recurrence Score as a *predictor* of clinical
  response, not a treatment effect.
- **TRYPHAENA** — primary endpoint was cardiac safety; the pCR figures across
  three arms are descriptive.
- **DeLLphi-305** — the OS figure is a cross-trial comparison against IMP133.

---

## 2. Direction traps — please double-check these

- **INT-0116 (left fully unmarked).** The HRs are inverted: OS HR **1.32**
  (1.10–1.60; P=.0046) with median OS 36 vs 27 months favouring
  chemoradiation. The HR is expressed for the surgery-only arm, so HR > 1 means
  the *study* arm won. Marking this mechanically would have produced a ❌ on a
  positive trial. Worth rewriting the cell to state the direction explicitly.
- **RAPIDO (marked ✅).** "3yr DrTF 23.7% vs 30.4%" is a *failure* rate — lower
  is better, so the smaller number is the good result. Correct as marked, but the
  cell reads backwards at a glance.
- **NIAGARA.** The cell says "pCR **HR** 1.30 (1.09–1.56)" — that is an odds
  ratio, not a hazard ratio, and >1 is favourable here. Marked ✅. Suggest
  relabelling to OR.
- **KRISTINE.** Ordering is experimental-first, so pCR 44.4% vs 55.7% and EFS
  HR 2.61 mean the *experimental* arm did worse. Marked ❌ accordingly — please
  confirm the arm order is as I read it.
- **CASPIAN (PFS).** HR 0.78 (0.65–0.94) is significant, but the medians read
  5.1 vs 5.4 — i.e. the median favours the control while the HR favours
  durvalumab. Marked ✅ off the HR; flagging because the row looks contradictory.
- **CAIRO5.** Left unmarked — I could not determine whether the "9.0 vs 10.6"
  ordering matches the HR direction.
- **Gem-carbo.** Left unmarked — PFS medians (5.8 vs 4.2) favour arm 1 but
  HR 1.04 points the other way. One of the two is wrong.

---

## 3. Trials that missed a prespecified boundary (marked ⚠️, not ✅)

These look significant by naive p<0.05 but did **not** meet their own alpha:

- **KN-224/240** — OS p=0.0238 vs boundary 0.0174; PFS p=0.0022 vs 0.002. Both missed.
- **LEAP-002** — OS p=0.023 vs boundary 0.0185.
- **KN-355** — PFS/OS significant in CPS ≥10 only; CPS ≥1 and ITT not formally met.
- **KN-177 (OS, left unmarked)** — the cell shows HR 0.73 (0.53–0.99) but
  KEYNOTE-177's final OS did **not** cross its boundary. Please verify which
  analysis this row refers to before it gets a ✅.
- **INAVO-120 (OS)** — same shape as EMERALD, and this row may simply be out of
  date. The results table gives interim OS HR 0.64 (0.43–**0.97**), P=0.03, and
  labels it *"not significant per interim boundary"* — so I marked ⚠️. But the
  row's own **Key takeaway** already says *"2025 ASCO: OS benefit"*, which
  suggests a later, positive OS readout exists that the `mOS`/`HR` cells have
  not been updated with. If you add the final OS figures, both lines become ✅.
- **EMERALD (OS)** — ESR1-mut p=.03 is flagged NS in the cell (interim alpha).
  Applied as ⚠️. Worth flagging as the clearest counterexample to the
  "CI excludes 1 → ✅" shortcut: HR 0.59 (0.36–0.96) *does* exclude 1, yet the
  Haybittle-Peto interim boundary was α=.0001, so the result is not significant.
  Both EMERALD OS lines are ⚠️ for this reason, not because the CI crosses 1.

---

### 3a. Borderline CIs resting on 1.00 — RESOLVED, now ✅

**Your decision: these are green checks.** A CI bound sitting on (or a hundredth
past) 1.00 does not by itself make a result negative when the trial met its own
significance level and the effect is clinically meaningful. Applied:

| Row | Cells changed | Statistic |
|---|---|---|
| FLAURA | `mOS`, `HR` OS line | HR 0.80 (0.64–**1.00**), p=0.046 vs prespecified alpha 0.0495 — boundary met |
| MONALEESA-3 | `mOS` and `HR`, both the 1L and 2L lines | 1L HR 0.70 (0.48–**1.02**); 2L HR 0.73 (0.53–**1.00**), under a significant ITT (HR 0.72, P=0.00455) |

The rule in `SKILL.md` has been rewritten to match, so future `/add-trial`
entries follow it automatically. **⚠️ now means only** "failed its own
prespecified test, was never formally tested, or is immature" — it no longer
means "CI touches 1". Rows still ⚠️ for the genuine reason are unaffected
(KEYNOTE-224/240, LEAP-002, EMERALD interim OS, INAVO-120 interim OS).

**One thing to look at.** MONALEESA-3's 1L CI is **0.48–1.02**, which crosses 1
rather than resting on it, so unlike the other three that line is not
statistically significant on its own terms. I applied ✅ as instructed — the
reading is defensible (prespecified subgroup, significant ITT, same direction as
2L) — but it is the one cell of the four where ✅ asserts something the subgroup
statistic alone doesn't support. Say the word and I'll put that single line back
to ⚠️ and leave the other three green.

---

### 3b. The reverse case — endpoint met, later look labelled "descriptive"

- **EMILIA (OS)** — the cell holds two lines: the 2nd interim (30.9 vs 25.1,
  HR 0.68, P<0.001) and the final analysis (29.9 vs 25.9, HR 0.75, descriptive,
  27% crossover). I marked **both ✅**. The final analysis is "descriptive" only
  because OS had already been declared positive at the interim and the alpha was
  spent — not because the result is in doubt (HR 0.75, CI 0.64–0.88, still
  excludes 1). Marking the second line ⚠️ would have implied EMILIA's OS benefit
  is uncertain, which is wrong. Flagging it in case you'd rather it read ⚠️ to
  signal "not formally tested".

---

## 4. Primary endpoints that failed (marked ❌ — sanity-check these)

- **FIRE-3** — primary endpoint was **ORR** and it failed (OR 1.18, p=0.18),
  despite the well-known OS benefit. ORR ❌, OS ✅ on the same row.
- **TRIPLETE** — primary ORR failed (OR 0.87, P=.526).
- **AVANT** — bevacizumab arms were *worse*: OS HR 1.27 (1.03–1.57), p=0.02.
- **CAIRO2** — PFS HR 1.22 (1.04–1.43), p=0.01 — significantly worse.
- **PARSIFAL** — PFS HR 1.13, P=.32; did not meet its endpoint.
- **KRISTINE** — see direction note above.
- **APHINITY (node-negative)** — iDFS HR 1.01 (0.72–1.42), no benefit.
- **HERA** — 2-yr vs 1-yr trastuzumab DFS HR 1.02, no added benefit.

---

## 5. Data-quality issues found along the way (unrelated to symbols)

| Row | Issue |
|---|---|
| MONALEESA-3 | `PFS (month)` says 2L = **14.6**; the page-body table says **14.9**. One is wrong. |
| EV-302 | `OS HR 0.47` paired with CI **(0.63-0.96)** — the CI cannot contain the point estimate. Likely a typo. |
| EV-302 | Three different median OS values appear on the row/page: the `mOS` property says **33.6**, the primary-endpoint table says **31.5**, and the 2.5-year update says **33.8**. The property matches none of them. (Also note the 2.5-yr update's own HR reads "0.61, 0.43-0.61" — upper bound equals the point estimate, so that one is mistyped too.) |
| IMpower 010 | ITT DFS HR appears as **0.81 (0.67-0.99)** in the DFS cell but **0.85 (0.71–1.01)** in the HR cell — these disagree on significance. Left the HR cell unmarked. |
| Gem-cis | `PFS` reads "7.7 vs **8,3**" — comma instead of decimal point. |
| ADRIATIC | ORR 30.3% vs 32.0% favours the control arm; left unmarked as there is no test, but worth a note in the row. |
| BREAKWATER | ORR is the primary endpoint; the cell has no p-value but the page body gives **OR 2.44, P<0.001**, so it *was* marked ✅. Consider adding the statistic to the cell itself. |
| CM-77T, CM-816, KN-671, KN-905/EV-303, MATTERHORN, FLOT4, RAPIDO, PICC | pCR reported without a p-value; several of these were significant in publication. Adding the statistic would let them be marked. |
| CALGB-SWOG 80405 | The `HR (95% CI)` cell says **OS HR 0.92 (0.78–1.09), p=0.34**, but the page-body table says **OS HR 0.88 (0.77–1.01), P=0.08**. Two different analyses or a transcription error — please reconcile. **Update:** the FIRE-3 page's own comparison table independently gives CALGB OS as "30.0 vs. 29.0 months (HR 0.88; P=0.08)", which agrees with the CALGB *body* — so the **0.92 / p=0.34 in the HR cell is the outlier** and is the value most likely wrong. |
| CALGB-SWOG 80405 (ORR reversal, confirmed) | The FIRE-3 page also lists CALGB ORR as "59.6% vs. 55.2% (P=0.13)" with cetuximab first — confirming the CALGB row's ORR cell has its arms **reversed**. |
| CALGB-SWOG 80405 | `ORR` reads "55.2% vs. 59.6%" but `Drug/Control` is "Cetuximab vs. bevacizumab" and the body gives cetuximab **59.6%** / bev **55.2%** — the arms in the ORR cell are **reversed** relative to every other cell in the row. Left ORR unmarked because of this. |
| CM-8HW | `HR (95% CI)` reads **"PFS 0.21 (0.33-0.35)"** — the confidence interval does not contain the point estimate, so one of the two is a typo. |
| HIMALAYA | The `HR (95% CI)` cell gives STRIDE OS as **0.78 (0.63-0.99)**, but the `mOS` cell and the page body both give **0.78 (0.67-0.92)**. Same point estimate, two different CIs — one is a transcription error. |
| IMpower133 | The PFS p-value appears twice on the page with different values: the results table says **p=0.002**, the KM figure caption says **P=0.02**. (Published value is 0.02.) ✅ either way. |
| IMpower133 | `ORR` reads **60.2 vs. 64.4** — the *control* arm responded more often, even though PFS and OS both favour atezolizumab. No test is reported so it is left unmarked, but the row reads oddly next to two ✅s. Same shape as the ADRIATIC ORR note above. |
| IMbrave 150 | The `ORR` cell gives mRECIST as **35 vs. 14**, but the page body gives **33.2% vs 13.3%**. Both are ✅ either way (p<0.001), but the numbers should agree. |
| CASPIAN | The `ORR` cell gives only the durvalumab arm ("79% unconfirmed; 68% confirmed") with no comparator. Marked ✅ because the underlying comparison is significant (OR 1.64, 1.11–2.44 vs 70%), but the cell should carry both arms. |
| DESTINY-Breast03 | The page body attaches **P=0.0037** to two different OS hazard ratios: the Discussion says "OS met significance at 2nd interim (**HR 0.64**; P=0.0037)" while the results table says **HR 0.73 (0.56–0.94); P=0.0037**. 0.64 is the Lancet 2023 2nd-interim figure and 0.73 is the Nat Med 2024 long-term figure — the p-value belongs only to the former. Both are ✅ either way, but the pairing should be fixed. |
| DESTINY-Breast03 | `HR (95% CI)` gives PFS **0.28 (0.22–0.37)** while the body table gives PFS BICR **0.33 (0.26–0.43)**. Not an error — different data cutoffs (NEJM 2022 primary vs Lancet 2023 update) — but the cell doesn't say which, so it reads as a contradiction. |

---

## 6. Cells that would need splitting to be marked properly

These pack several populations onto one line, so a single symbol would be
misleading. Left unmarked or partially marked:

- **CAPItello-291 (OS)** — "29.4 vs 28.6 (overall); 28.5 vs 30.4 (AKT-alt)" on
  one line, where overall is ❌ and AKT-altered is ⚠️.
- **EMERALD (OS)**, **HIMALAYA (PFS)**, **KN-048**, **SOFT** (3-arm),
  **ARTIST 2** (3-arm), **MARIPOSA-2 (OS)**, **GERCOR**, **PARADIGM (PFS)**.
- **CM-8HW (PFS)** — "24M 72% vs. 55% vs. 14%" packs both dual primary
  comparisons onto one line with *opposite* verdicts: nivo-ipi **vs chemo** was
  positive (HR 0.21, p<0.0001 → ✅), but nivo-ipi **vs nivo monotherapy** missed
  its boundary (p=0.0413 vs 0.0383), so dual-IO superiority could not be
  declared. Left unmarked — a single symbol would assert the wrong thing.
- **FALCON** — only the ITT line is marked; non-visceral and visceral subgroups
  have no separate statistics in the row.

Splitting these onto separate `<br>` lines (as MONALEESA-3 now is) would let each
population carry its own verdict.
