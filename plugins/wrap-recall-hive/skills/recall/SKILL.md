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

**Read root:** this seat’s pack only (e.g. `~/.claude/claude-memory/`, `~/.grok/memory/`, or `~/.agent-memory/<seat>/`).  
Crew search is **`/hive`** — not this skill.

## Budget

| Target | Guidance |
|--------|----------|
| Sweet spot | ~30k–50k tokens |
| Floor | Spine + at least one latest `## Recall` |
| Ceiling | Cap ~50k; drop older journals before spine |

## Procedure

### Blank focus

1. Spine  
2. Latest 1–3 journal `## Recall` sections only  
3. Today’s worklog tail  
4. Stop at budget  

### Focus provided — **own pack only**

Search journal + worklog for the stub; load matching Recalls. Prefer relevance. If empty, fall back to blank pack and say so.

### Do not load as autobiography

- `## From the hive` — peer evidence only (keep owner labels)  
- Other seats’ packs (use `/hive`)  
- Secrets / full transcripts  

### Report

```markdown
## Recall loaded

**Focus:** <none | note>
**Loaded:** …
**Carry-forward:** 3–8 bullets
**Open threads:** …
```

Read-only. Do not wrap unless asked.
