---
description: Rebuild the Trial Recall flashcard deck from the Notion oncology databases — cards any trial added or edited since the last sync, then republishes the deck.
argument-hint: "[trial name or Notion URL — optional, defaults to a full sync]"
---

Sync the Trial Recall flashcard deck with the Notion oncology databases.

Target: $ARGUMENTS

Delegate this to the **flashcard-writer** subagent.

- If a trial name or Notion URL was given above, tell the agent to card exactly
  that trial (targeted mode). Resolve a bare name to its Notion page URL first.
- If nothing was given, tell the agent to run a full sync: pull both databases,
  diff against `deck/deck.json`, and write cards only for what changed.

Before delegating, show the user what is pending so they know the size of the
run, using the most recent `rows.json` if one exists from this session:

```bash
python3 deck/sync.py plan <rows.json>   # only if a fresh pull already exists
```

Otherwise let the agent do its own pull.

When the agent reports back, relay to the user: the counts of new and updated
cards with trial names, the deck URL, and anything the agent flagged — thin
Notion rows, takeaways it had to author itself, or trials that disappeared from
Notion. Do not let a "GONE from Notion" finding pass silently; a card is only
deleted after the user confirms.
