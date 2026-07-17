---
name: recall
description: >
  Start-of-session memory reload. Load your own memory pack (spine + journal
  Recalls + worklog) so a cold session continues without replaying transcripts.
  Target ~30–50k tokens. Use on recall, /recall, remember, load memory, or after clear/new.
argument-hint: "[optional focus: what to remember / look for]"
---

# Recall — load your own memory pack

**Keywords:** `recall` · `remember` · `load memory` · `/recall` · `/recall <focus>`  
**Read root (default example):** `~/.agent-memory/<your-seat>/`

This is the **load** twin of `/wrap`. Crew / multi-seat search is **`/hive`** — not this skill.

## Budget (hard rule)

| Target | Guidance |
|--------|----------|
| Sweet spot | ~30k–50k tokens loaded |
| Floor | Spine + at least one latest `## Recall` if they exist |
| Ceiling | Cap ~50k tokens; drop older journals / worklog tails before the spine |

Rough size: ~4 chars ≈ 1 token.

## Procedure

### 0. Orient

1. Confirm pack root exists.  
2. List journal filenames (newest first).  
3. Note whether focus is empty or set.

### 1A. Blank focus — recent default pack

1. **Spine** — full (or skim if huge).  
2. **Latest journal `## Recall` only** — last 1–3. Prefer `## Recall` through next `##`, not full multi-page Notes.  
3. **Today’s worklog** tail (or yesterday if today empty).  
4. Stop at budget.

### 1B. Focus provided — search **own pack only**

1. Spine still first (self remains self).  
2. Search journal + worklog for keywords (filenames, Recall bodies, worklog titles).  
3. Load matching Recalls / worklog blocks.  
4. Prefer relevance over dumping entire history.  
5. If nothing matches: say so, then fall back to §1A.

### 2. What not to load

- Full `## Notes` when `## Recall` already carries the judgment  
- Transcripts / session JSONL as if they were wrap memory  
- Secrets, auth files  
- **`## From the hive` as autobiography** — peer evidence only; load when focus needs it and keep owner labels  
- Other seats’ packs (use `/hive`)

### 3. Report

```markdown
## Recall loaded

**Focus:** <none | note>
**Loaded:** spine / journal slugs / worklog
**Approx size:** …
**Carry-forward:** 3–8 bullets
**Open threads:** …
```

Read-only on the pack. Do not wrap unless asked.

## Pair

| Cue | Tool |
|-----|------|
| Distill this session | `/wrap` |
| Load *my* continuity | `/recall` |
| Search the *crew* | `/hive` |
