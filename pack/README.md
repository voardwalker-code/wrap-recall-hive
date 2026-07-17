# Memory pack layout

Each **seat** (agent identity) owns exactly one pack root.

```
<pack-root>/
  README.md                 # load order + do-nots
  relationship-spine.md     # durable who/how/agreements/lore
  journal/
    YYYY-MM-DD-slug.md      # ## Recall + ## Notes + ## From the hive
  worklog/
    YYYY-MM-DD.md           # daily facts
```

## Suggested roots

| Seat | Example path |
|------|----------------|
| Primary coding agent | `~/.agent-memory/primary/` |
| Second agent | `~/.agent-memory/secondary/` |
| Project-scoped seat | `~/projects/my-sandbox/memory/` |

**Do not** commit live packs to a public git remote. Packs hold personal judgment, paths, and relationship context.

## Load order (`/recall`)

1. Spine  
2. Latest journal `## Recall` section(s)  
3. Today’s worklog tail  
4. Budget ~30–50k tokens  

## Write order (`/wrap`)

1. New journal file (or append same-task slug)  
2. Worklog block  
3. Spine only if durable truth changed  
