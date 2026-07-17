---
name: wrap
description: >
  End-of-session memory ritual. Distill this session into your own memory pack
  (journal + worklog + relationship spine) so the next session can reload
  cheaply (~30–50k tokens, not a full transcript). Use on wrap, /wrap, wrap up,
  goodnight, or before /clear or /new.
argument-hint: "[optional note about what to emphasize]"
---

# Wrap — end-of-session memory ritual

**Keywords:** `wrap` · `wrap up` · `/wrap` · `goodnight` · `save the memory`  
**Write root (default example):** `~/.agent-memory/<your-seat>/`  
Configure your real path in the tool skill or environment; **never** write into another seat’s pack.

This is **judgment distillation**, not a transcript dump. Do it **before** clear/new.

**Pair:** next session loads with **`/recall`**. Crew search is **`/hive`** (separate tool).

## Pack layout

| Layer | Path | Role |
|-------|------|------|
| Spine | `relationship-spine.md` | Durable agreements, lore, how the human asks |
| Journal | `journal/<YYYY-MM-DD>-<slug>.md` | Distilled `## Recall` + notes |
| Worklog | `worklog/<YYYY-MM-DD>.md` | Facts / paths / status |
| Index | `README.md` | Load order + do-nots |

## Procedure

### 0. Orient

1. Skim the spine if it exists.  
2. List recent journal filenames (avoid duplicate slugs).  
3. Today’s date + kebab slug for this task.

### 1. Journal (required)

```markdown
## Recall

<1–3 tight paragraphs for the NEXT cold session.
ONLY what THIS seat and the human did / decided this session.
HARD FENCE: never narrate other agents’ work as "we" or "I".
Peer trails go in ## From the hive only.>

## Notes

### What happened
- …

### Artifacts / paths
- …

### Explicit non-goals / do-nots
- …

### Open threads
- …

## From the hive

<If /hive was used OR peer packs were read: fill the form.
If neither: write exactly _No hive consult this session._>

### Hive consults this session
- **Focus / cue:** …
- **CLI / path:** `python3 path/to/hive.py --focus "…"`
- **Owners hit:** …

### Peer trails (attributed — not me)
- **[owner=… · when=… · kind=…]** <what *they* did> · source: `…`

### What I take from them (my application only)
- … or _none_

### Peer relationship notes (optional)
- … how *this seat's* working relationship with that peer shifted
```

### 2. Worklog (required)

```markdown
### W— — <short title>
**Ask:** …
**Did:**
- … (own actions; peer cites attributed)
**Hive:** none | focus "…" · owners: …
**Status:** Done | Partial | Blocked
**Touched:** paths…
**Not done:** …
```

### 3. Spine (only if durable change)

Edit only for lasting agreements, ask-patterns, lore, machine facts, or **peer seat relationships**.  
If peer truth is durable, maintain `## Peer seats (crew)` — **from this seat’s side only**. Do not write into another pack (visa versa = their wrap).

### 4. Confirm

Report journal path, worklog path, spine updated/unchanged, hive section status.  
Do not clear the session unless asked.

## Anti-patterns

- Transcript dump  
- Folding hive/peer work into `## Recall` as autobiography  
- Omitting `## From the hive` after a hive session  
- Cross-writing another seat’s pack  
- Secrets / API keys / auth files in any layer  
