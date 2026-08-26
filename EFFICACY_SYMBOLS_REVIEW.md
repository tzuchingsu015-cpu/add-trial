# Efficacy symbol pass — items needing your review

Legend applied across both databases:

| Symbol | Meaning |
|---|---|
| ✅ | Statistically significant benefit — endpoint met (p below the prespecified boundary, or HR 95% CI excluding 1) |
| ⚠️ | Numerically favorable but **not** statistically significant, not formally tested, or immature |
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

Note REFLECT and STELLAR are the interesting ones: non-inferior on the primary
endpoint but genuinely *superior* on a secondary, so the row now carries **↔**
and ✅ side by side — which is the correct reading of both trials.

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
- **EMERALD (OS)** — ESR1-mut p=.03 is flagged NS in the cell (interim alpha).

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
| IMpower 010 | ITT DFS HR appears as **0.81 (0.67-0.99)** in the DFS cell but **0.85 (0.71–1.01)** in the HR cell — these disagree on significance. Left the HR cell unmarked. |
| Gem-cis | `PFS` reads "7.7 vs **8,3**" — comma instead of decimal point. |
| ADRIATIC | ORR 30.3% vs 32.0% favours the control arm; left unmarked as there is no test, but worth a note in the row. |
| BREAKWATER | ORR is the primary endpoint; the cell has no p-value but the page body gives **OR 2.44, P<0.001**, so it *was* marked ✅. Consider adding the statistic to the cell itself. |
| CM-77T, CM-816, KN-671, KN-905/EV-303, MATTERHORN, FLOT4, RAPIDO, PICC | pCR reported without a p-value; several of these were significant in publication. Adding the statistic would let them be marked. |
| CALGB-SWOG 80405 | The `HR (95% CI)` cell says **OS HR 0.92 (0.78–1.09), p=0.34**, but the page-body table says **OS HR 0.88 (0.77–1.01), P=0.08**. Two different analyses or a transcription error — please reconcile. |
| CALGB-SWOG 80405 | `ORR` reads "55.2% vs. 59.6%" but `Drug/Control` is "Cetuximab vs. bevacizumab" and the body gives cetuximab **59.6%** / bev **55.2%** — the arms in the ORR cell are **reversed** relative to every other cell in the row. Left ORR unmarked because of this. |
| CM-8HW | `HR (95% CI)` reads **"PFS 0.21 (0.33-0.35)"** — the confidence interval does not contain the point estimate, so one of the two is a typo. |
| CASPIAN | The `ORR` cell gives only the durvalumab arm ("79% unconfirmed; 68% confirmed") with no comparator. Marked ✅ because the underlying comparison is significant (OR 1.64, 1.11–2.44 vs 70%), but the cell should carry both arms. |

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
