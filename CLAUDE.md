# add-trial

This repo holds the `add-trial` Claude Code skill (`skills/add-trial/SKILL.md`),
which reads a clinical-trial reference attachment and creates a structured
entry in one of two Notion oncology databases (Early Stage Cancer Database /
Metastatic Cancer Database). See `README.md` for the overview and
`skills/add-trial/SKILL.md` for the full routing rules, schemas, and workflow
— that file is the source of truth; keep this memory in sync with it rather
than duplicating its detail.

## Standing requirement: FDA approval check on every trial added

Whenever a trial is added or updated via this skill, look up the drug/regimen's
**current** FDA approval status for the trial's indication (web search, not
training-data memory — approvals change) and:

1. Record the approval facts in the page's `Discussion/Notes` section: approved
   or not, regular vs. **accelerated** approval, and whether the **approved
   population** matches the trial's **primary-endpoint population**.
2. If the trial result and the approval status are **discordant** — a positive
   trial with only accelerated approval, approval for a narrower/different
   population than the primary endpoint, or no approval at all; or a
   **negative** trial that's FDA-approved anyway — prefix a `Key takeaway`
   line with `⚠️` and state the discordance in words.
3. Otherwise (concordant), no flag is needed, but the approval facts still go
   in Discussion/Notes.

Full detail: `skills/add-trial/SKILL.md`, Workflow step 8 ("Check FDA approval
status") and the "FDA discordance marker" bullet under "Property value
conventions".
