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

## Non-goals

- Vendor lock-in to one agent CLI  
- Silent cross-write  
- RAG over full transcripts as the continuity product  
- Storing secrets in packs  

## Related systems

This package is **session continuity for coding agents** only.  
Orchestrators, companion minds, and full cognitive OS work are separate products; list them in `RELATED.md` only when a shareable cut is intentional.
