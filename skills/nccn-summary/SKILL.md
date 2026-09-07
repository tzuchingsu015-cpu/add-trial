---
name: nccn-summary
description: Use when the user supplies an NCCN Clinical Practice Guideline PDF (or a Drive link to one) and wants a focused summary of one disease subset — e.g. "isolate the early HR-positive breast cancer part", "summarize the BINV section", "break the management into preoperative and adjuvant". Produces an HTML artifact in which every algorithm recommendation carries the Discussion evidence and rationale behind it, plus a trial summary table.
argument-hint: <disease subset, e.g. "early HR-positive breast cancer">
---

# NCCN Guideline Subset Summary

Turn one subset of an NCCN guideline into a standalone HTML artifact that
answers not only *what* the algorithm says but *why it says it*.

## The rule that defines this skill

The algorithm pages (BINV-n, and their equivalents in other guidelines) give
the conclusion and a citation list, with no results. The Discussion (MS-n)
carries the trials, the numbers, the negative studies, and the reasoning.
A summary of the algorithm alone gives the user a crude conclusion they
could have read themselves.

**So: no recommendation ships without its evidence.** For every decision node
you carry over from the algorithm, go find the matching Discussion passage
and attach two things — what the trials showed, and why the recommendation
is worded the way it is (why a hedge, why a category 2B, why an alternative
option is offered, why a cutoff sits where it does). If you cannot find the
rationale in the Discussion, say so on that node rather than omitting it.

This is a standing preference of this user, not a per-request option.

## Getting the PDF into the environment

Direct `curl` to `drive.google.com` is blocked by egress policy (exit 56,
`connect_rejected`). Route through the Google Drive MCP tools instead:

1. `get_file_metadata` on the file id from the share link — confirm title,
   size, page count.
2. **Do not use `read_file_content`.** It silently truncates: on a 278-page
   guideline it returned ~335k characters and stopped mid-document, dropping
   the entire Discussion without any error. A summary built on that output
   will be missing exactly the part this skill exists to extract.
3. `download_file_content` → the harness saves the oversized result as JSON
   under `~/.claude/projects/.../tool-results/*.txt`. Pull the base64 payload
   out of that file and decode it to a local `.pdf` in the scratchpad.
4. `pip install pymupdf` works (PyPI is reachable).

Verify the page count of the decoded file matches the metadata before
extracting anything.

## Extraction

Discussion pages are two-column; ordinary PyMuPDF extraction interleaves the
columns into gibberish. Use the bundled column-aware extractor:

```
python3 scripts/extract_columns.py <pdf> <first> <last> --offset N
```

Pages are 0-based PDF indices, last exclusive. Find the offset once by
locating MS-1 and subtracting; in Breast Cancer v6.2026, MS-1 was PDF index
127, so `--offset 126`. Algorithm pages are single-column enough that the
same script reads them fine.

Dump the whole Discussion and the reference list to files up front — you
will grep them repeatedly.

## Mapping the guideline before you write anything

Build a page map first; the rest of the work is lookups against it.

| Page type | What it holds | Use it for |
|---|---|---|
| `XXXV-n` algorithm pages | Decision boxes, footnotes, citation superscripts. No results. | The node list — the skeleton of the summary |
| `XXXV-<letter>` principles pages | Detail on one modality (regimens, assays, RT technique) | Filling in a node's specifics |
| `MS-n` Discussion | Narrative, trial names, numbers, negative trials, panel reasoning | **The evidence and rationale for every node** |
| Reference list | Full citations by number | Resolving the algorithm's superscripts to real trials |

Then, for each algorithm node, record the MS page range that discusses it.
That mapping is the working document; write from it, not from memory.

## Output structure

An HTML artifact (load `artifact-design` before writing it). Sections, in
this order:

1. **Scope** — exactly which guideline, version, date, and which pages the
   summary covers; what is deliberately excluded.
2. **Stratification** — how the guideline sorts patients into this subset.
3. **Why the algorithm reads this way** — the heart of the deliverable; see
   the node-card format below.
4. **Assays / biomarkers**, if the subset has them.
5. **Management, split into preoperative and adjuvant**, each broken down by
   treatment category (chemotherapy, endocrine, CDK4/6 or other targeted,
   PARP, bone-modifying, RT, surgery).
6. **Trial summary table** — trial/reference name, patient population,
   efficacy results. Frame it as a lookup index that points back into the
   rationale section, not as the main content.
7. **Open questions / where the guideline is silent.**

### Node card format

One card per decision node, laid out with the trial names on a strip above
the box — this echoes the flowchart style the user works from, where each
decision carries its evidence on its face.

```html
<article class="node q">
  <div class="node-trials">RxPONDER &mdash; the ovarian suppression confound</div>
  <div class="node-rec"><span class="lbl">Node &mdash; premenopausal, RS &lt;26</span>
    Chemotherapy then endocrine therapy, <b>or alternatively OFS + tamoxifen or an AI</b></div>
  <div class="node-body">
    <p><b class="tag">Evidence</b>… what the trial showed, with numbers …<span class="src">MS-40/43</span></p>
    <p><b class="tag why">Why an endocrine option is offered instead</b>… the panel's reasoning …</p>
  </div>
</article>
```

Colour the trial strip by what the evidence does:

- default (accent) — the trial that establishes the recommendation
- `.q` (clay) — the node is deliberately hedged, and the strip names the
  reason for the hedge
- `.neg` (slate) — a negative or restrictive result is what shapes the node

## Provenance: two tiers, always visible

Every efficacy figure must declare where it came from.

- A figure **printed in the guideline itself** gets a badge naming the page
  (`MS-40`, `BINV-N 3`). These are the reliable ones.
- A figure recalled from the **primary publication** and not found in the
  guideline text gets no badge and is explicitly marked as needing
  verification against the source paper.

Never blur the two. In the first pass of the breast cancer summary, remembered
figures for monarchE, NATALEE and OlympiA all had to be replaced with NCCN's
own numbers once the Discussion was actually read.

## Flag algorithm/Discussion divergence

The Discussion is revised on its own cycle and can lag the algorithm pages by
years — in Breast Cancer v6.2026 the algorithm was dated 07/29/26 while the
Discussion was stamped as updated 06/07/24. Where they disagree:

- **The algorithm page is current. The Discussion is the historical rationale.**
- Say so on the node, with both dates, rather than silently picking one.

In that guideline the divergences were: NSABP B-51 / regional nodal irradiation
after cN1→ypN0; SLNB omission (SOUND/INSEMA); RT instead of endocrine therapy
in older patients (EUROPA); and olaparib eligibility including the CPS+EG
criterion. Expect a handful like these in any guideline.

## Category semantics — carry them, don't flatten them

`Category 1`, `2A`, `2B` and `3` are statements about the panel's consensus and
the evidence level, and the Discussion usually explains which one applies and
why. A 2B often reflects an implementation problem rather than weak data (RCB
is 2B because reporting is inconsistent across institutions, not because the
data are poor). Preserve the category on the node and explain it.

## Licensing

NCCN PDFs carry a EULA in the page footer stating the content may not be
distributed or used with an AI model or tool. Flag this to the user once, in
one sentence, the first time you work on one — then leave the decision about
use and circulation to them. Produce a **reorganized clinical synthesis with
the trial evidence attached**; do not reproduce guideline pages verbatim, and
strip the footer boilerplate from extracted text (the bundled script does this).

## Checklist before delivering

- [ ] Every node has Evidence *and* Why-it-reads-this-way.
- [ ] Every number is either badged to a guideline page or marked unverified.
- [ ] Negative and restrictive trials are present, not just the positive ones.
- [ ] Algorithm/Discussion divergences are named with both dates.
- [ ] Preoperative and adjuvant are separated; treatments are grouped by class.
- [ ] The trial table's populations match what the trial actually enrolled —
      this is what explains why a recommendation stops where it stops.
- [ ] Artifact themes correctly in light, dark, and system (every colour a
      token defined in all three theme blocks).
