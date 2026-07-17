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

**Write root:** configure per seat (examples: `~/.agent-memory/<seat>/`, Claude often uses `~/.claude/claude-memory/`, Grok often uses `~/.grok/memory/`).  
**Never** write into another seat’s pack.

**Pair:** next session **`/recall`**. Crew search **`/hive`** (separate).

## Pack layout

| Layer | Path | Role |
|-------|------|------|
| Spine | `relationship-spine.md` (or `RELATIONSHIP.md`) | Durable agreements, lore |
| Journal | `journal/<YYYY-MM-DD>-<slug>.md` | `## Recall` + notes + hive |
| Worklog | `worklog/<YYYY-MM-DD>.md` | Facts / paths / status |

## Procedure

### 0. Orient

1. Skim the spine if present.  
2. List recent journal filenames (avoid duplicate slugs).  
3. Today’s date + kebab slug.

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

<If /hive used OR peer packs read: fill form.
If neither: write exactly _No hive consult this session._>

### Hive consults this session
- **Focus / cue:** …
- **CLI / path:** …
- **Owners hit:** …

### Peer trails (attributed — not me)
- **[owner=… · when=… · kind=…]** <what *they* did> · source: `…`

### What I take from them (my application only)
- … or _none_

### Peer relationship notes (optional)
- …
```

### 2. Worklog (required)

```markdown
### W— — <short title>
**Ask:** …
**Did:**
- …
**Hive:** none | focus "…" · owners: …
**Status:** Done | Partial | Blocked
**Touched:** paths…
**Not done:** …
```

### 3. Spine (only if durable change)

Including **peer seat relationship** rows when lasting. Do not cross-write other packs.

### 4. Confirm

Report journal path, worklog path, spine updated/unchanged, hive section status.

## Anti-patterns

- Transcript dump · folding hive into `## Recall` · secrets in packs · cross-write  
