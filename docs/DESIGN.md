# Design brief — wrap / recall / hive

## Problem

Coding agents lose continuity after `/clear` or a new session. Transcript replay is expensive and noisy. Multi-agent crews also re-solve problems another seat already wrapped — or worse, melt peer work into “I did that.”

## Solution (three tools)

| Tool | Direction | Scope |
|------|-----------|--------|
| **`/wrap`** | Session → disk | **Own** pack only (distill) |
| **`/recall`** | Disk → session | **Own** pack only (budgeted load) |
| **`/hive`** | Disk → session | **Crew** packs + shared files (opt-in, labeled) |

**Do not** replace wrap/recall with automatic whole-house search. That becomes a noise vacuum and corrupts identity.

## Pack layers

1. **Spine** — durable relationship + agreements  
2. **Journal** — `## Recall` (own) + `## Notes` + `## From the hive` (peer)  
3. **Worklog** — daily facts + `**Hive:**` line  

## Hive

- Registry maps `owner id → root path`  
- CLI searches journals/worklogs/spines/shared files  
- Output is budgeted markdown with `not_me=true` envelopes  
- Stdlib Python; no cloud required  

## Install surface (M17)

Rituals must stay three plain names: **`wrap` · `recall` · `hive`**.

| Host | Daily install | Avoid |
|------|---------------|--------|
| **Grok** | `./scripts/install-grok.sh` → `~/.grok/skills/` | `grok plugin install` *plus* loose skills (namespaced twin UI) |
| **Claude** | Marketplace plugin *or* `./scripts/install.sh --claude` | Both at once |

Plugin packaging exists for Claude marketplace distribution. It is not a second product and must not double the slash menu.

## Non-goals

- Vendor lock-in to one agent CLI  
- Silent cross-write  
- RAG over full transcripts as the continuity product  
- Storing secrets in packs  
- Dual install paths that show `package:skill` beside plain skill names on the same host  

## Related systems

This package is **session continuity for coding agents** only.  
Orchestrators, companion minds, and full cognitive OS work are separate products; list them in `RELATED.md` only when a shareable cut is intentional.
