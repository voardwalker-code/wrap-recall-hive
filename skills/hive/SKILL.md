---
name: hive
description: >
  Hivemind memory search across crew wrap packs and shared house files.
  Opt-in only — does NOT replace /wrap or /recall. Use when the user says hive,
  /hive, hivemind, or wants to audit another agent's journals with not-me labels.
argument-hint: "[focus: what to find in the crew's memories]"
---

# Hive — search the hivemind

**Keywords:** `hive` · `hivemind` · `/hive` · `/hive <focus>`  
**Runtime:** this package’s `hive/hive.py` + `hive/registry.json` (from example)

| Tool | Scope |
|------|--------|
| `/wrap` · `/recall` | **Your** pack only |
| `/hive` | **Crew + house** — labeled `not_me` |

## Product law

> You own your memories. When you want the hive, ask for it.  
> Every foreign span is **not your memory** — evidence for audit/apply.

## Procedure

### 0. Orient

```bash
python3 /path/to/wrap-recall-hive/hive/hive.py --list-owners
```

### 1. Search

```bash
python3 /path/to/wrap-recall-hive/hive/hive.py --focus "<focus note>"
python3 /path/to/wrap-recall-hive/hive/hive.py --focus "<note>" --from agent-b
```

Budget: default is fine; use `--budget-chars 80000` if context is already heavy.

### 2. Reason (required posture)

For every span with `not_me=true` / foreign `owner=`:

- Speak as **reviewer of their trail**, not as the author  
- Do not say “I shipped X” for their work  
- You may apply lessons; on wrap, put peer evidence under **`## From the hive`**  
- Do not write into their pack  

### 3. Report

```markdown
## Hive loaded

**Focus:** …
**Owners hit:** …
**Approx size:** …
**Carry-forward:** 3–8 bullets (attributed: who · what)
**Not-me discipline:** foreign trails used as evidence only
```

## What not to do

- Replace or extend `/recall` with house search  
- Auto-load hive on session start  
- Cross-write packs  
- Treat hive hits as autobiography  
- Require a specific IDE or cloud vendor  
