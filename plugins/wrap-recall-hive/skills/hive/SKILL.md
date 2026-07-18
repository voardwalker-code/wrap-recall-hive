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

| Tool | Scope |
|------|--------|
| `/wrap` · `/recall` | **Your** pack only |
| `/hive` | **Crew + house** — labeled `not_me` |

## Product law

> You own your memories. When you want the hive, ask for it.  
> Every foreign span is **not your memory** — evidence for audit/apply.

## Resolve the CLI

Try in order (first hit wins):

1. **Installer home (preferred):**  
   `python3 "${WRAP_RECALL_HIVE_HOME:-$HOME/.local/share/wrap-recall-hive}/hive/hive.py"`
2. **Claude Code plugin:**  
   `python3 "${CLAUDE_PLUGIN_ROOT}/hive/hive.py"`
3. **Dev clone:**  
   `python3 <repo>/hive/hive.py`
4. **Grok plugin (legacy only):**  
   `python3 "${GROK_PLUGIN_ROOT}/hive/hive.py"` — Grok daily install is loose skills (`install-grok.sh`), not this plugin (M17)

Registry: copy `hive/registry.example.json` → `registry.json` next to `hive.py` (or set `HIVE_REGISTRY`).

## Procedure

### 0. Orient

```bash
python3 "$CLI" --list-owners
```

### 1. Search

```bash
python3 "$CLI" --focus "<focus note>"
python3 "$CLI" --focus "<note>" --from agent-b
```

Budget: default is fine; use `--budget-chars 80000` if context is already heavy.

### 2. Reason (required posture)

For every span with `not_me=true` / foreign `owner=`:

- Speak as **reviewer of their trail**, not as the author  
- Do not say “I shipped X” for their work  
- On wrap, put peer evidence under **`## From the hive`**  
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
