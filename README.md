# wrap-recall-hive

**Own-pack session continuity for coding agents — plus an opt-in hivemind search for multi-seat crews.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> You own your memories. When you want the hive, ask for it. You never confuse the two.

| Ritual | Direction | Scope |
|--------|-----------|--------|
| **`/wrap`** | Session → disk | **Your** pack only (distill judgment) |
| **`/recall`** | Disk → session | **Your** pack only (~30–50k tokens, not 300k transcript) |
| **`/hive`** | Disk → session | **Crew** packs + shared house files (labeled `not_me`) |

This repository is a **shareable package**: agent skills, a stdlib Python hive CLI, pack templates, product laws, and synthetic demos.  
It is **not** a cloud service and **not** a full IDE.

---

## Why it exists

Coding agents are excellent until the context window dies, the human `/clear`s, or a second agent already solved the problem in another session.

Common “memory” products either:

- auto-extract trivia (“user likes TypeScript”) with no scar trails, or  
- RAG entire transcripts into a noise soup, or  
- melt multi-agent history into one identity (“I shipped that” — but Claude did).

**wrap-recall-hive** is a different product shape:

1. **Explicit distill** (`/wrap`) — you write what the *next* you needs.  
2. **Explicit load** (`/recall`) — budgeted own-pack continuity.  
3. **Explicit crew search** (`/hive`) — opt-in, attributed, never the default preseed.  
4. **Wrap hygiene** — peer evidence lands in `## From the hive`, never in own `## Recall`.

---

## Package contents

```
wrap-recall-hive/
├── README.md                 # this file
├── LICENSE                   # MIT
├── RELATED.md                # growing list of related open systems
├── skills/
│   ├── wrap/SKILL.md         # distill → own pack
│   ├── recall/SKILL.md       # load own pack
│   └── hive/SKILL.md         # search crew packs
├── hive/
│   ├── hive.py               # stdlib CLI (Python 3.10+)
│   ├── registry.example.json # template owner → path map
│   └── README.md
├── pack/                     # layout + examples for one seat
│   ├── README.md
│   ├── relationship-spine.example.md
│   ├── journal/EXAMPLE-*.md
│   └── worklog/EXAMPLE-*.md
├── examples/
│   ├── demo-pack/            # synthetic pack (safe to commit)
│   └── demo-registry.json    # points at demo-pack for smoke tests
└── docs/
    ├── LAWS.md               # M1–M16 product laws
    ├── DESIGN.md             # short design brief
    └── SECURITY.md           # privacy gate before going public
```

---

## Quick start

### 1. Clone

```bash
git clone <your-remote-url> wrap-recall-hive
cd wrap-recall-hive
```

### 2. Smoke-test hive (synthetic data — no personal packs)

```bash
python3 hive/hive.py --registry examples/demo-registry.json --list-owners
python3 hive/hive.py --registry examples/demo-registry.json --focus "rate limit"
```

You should see labeled spans with `owner=demo-a` and `not_me=true`, plus a **Hive report**.

### 3. Create your own pack

```bash
mkdir -p ~/.agent-memory/primary/{journal,worklog}
cp pack/relationship-spine.example.md ~/.agent-memory/primary/relationship-spine.md
cp pack/README.md ~/.agent-memory/primary/README.md
# edit the spine — it is yours
```

### 4. Install skills into your agent host

Copy or symlink skill folders into whatever your agent uses for skills, for example:

| Host | Typical skill root |
|------|--------------------|
| Grok Build | `~/.grok/skills/` |
| Claude Code | `~/.claude/skills/` |
| Codex | project `.agents/skills/` |
| Other | follow that product’s skill docs |

```bash
# example — adjust to your host
cp -R skills/wrap skills/recall skills/hive ~/.grok/skills/
```

Edit the skill paths if your pack root is not the default example (`~/.agent-memory/<seat>/`).

### 5. Optional multi-seat hive

```bash
cp hive/registry.example.json hive/registry.json
# edit roots for agent-a, agent-b, shared board/ledger paths
python3 hive/hive.py --list-owners
python3 hive/hive.py --focus "auth refactor"
```

**Do not commit** a `registry.json` that points at private personal trees if you later make this remote public. The package `.gitignore` is set up to help.

---

## How the three rituals work

### `/wrap` — distill

Write:

1. **Journal** — `## Recall` (own story only) + `## Notes` + **`## From the hive`**  
2. **Worklog** — facts + `**Hive:** none | focus · owners`  
3. **Spine** — only if a durable truth changed (including peer relationship rows)

If you used `/hive` this session, peer trails **must** go under `## From the hive` so the next `/recall` never thinks *you* shipped another agent’s work or owned their faceplant.

### `/recall` — load self

1. Spine  
2. Latest own `## Recall` sections  
3. Worklog tail  
4. Budget ~30–50k tokens  

Focused `/recall <note>` searches **your pack only**. Crew search is not this command.

### `/hive` — load crew (opt-in)

```bash
python3 hive/hive.py --focus "whatever stub the human half-remembers"
```

- Keyword search over registered roots  
- Budgeted assembly  
- Hard attribution headers  
- Audit posture: reason as reviewer of *their* trail  

**Why not bake hive into `/recall`?**  
House search on every continuity load becomes a noise vacuum (foreign journals, boards, half-hits) and breaks the lean pack that already works. Hive is a weapon you draw on purpose.

---

## Identity law (the part that makes multi-agent safe)

| Section | Whose story |
|---------|-------------|
| `## Recall` + `## Notes` | **This seat** + human |
| `## From the hive` | **Others** (evidence) + optional “what I take” |
| Spine `## Peer seats (crew)` | Durable relationship **to** peers — from this side only |

**Visa versa:** each seat records the others in *its own* spine. Nobody cross-writes packs to “stay symmetric.”

---

## Product laws (summary)

Full table: [`docs/LAWS.md`](docs/LAWS.md).

Highlights:

- Own write · no silent cross-write  
- Hive is additive (M15)  
- Wrap hive hygiene (M16)  
- Secrets never  
- Human gates on promote / destructive ops  

---

## Design notes

See [`docs/DESIGN.md`](docs/DESIGN.md) and [`docs/SECURITY.md`](docs/SECURITY.md).

**Intentional non-goals:** vendor lock-in, auto hive on session start, transcript RAG as continuity, companion “life memory” merged into coding packs, code-graph search (use a code indexer for that).

---

## Related projects (growing list)

Maintained in [`RELATED.md`](RELATED.md).

| Project | Role |
|---------|------|
| **wrap-recall-hive** (this) | Session continuity + hive search for coding agents |

Sibling house systems (orchestrator, cognitive substrate, …) get listed **when their public/replacement cut is ready** — not while rebuilds are private. See `RELATED.md` for how to add rows later.

---

## Privacy (why private first)

Live agent memory packs often contain:

- personal machine paths  
- private project names  
- relationship notes  

This **package** ships skills, CLI, synthetic demos, and docs only.  

Before flipping the GitHub repo to **public**:

1. Follow [`docs/SECURITY.md`](docs/SECURITY.md)  
2. `rg -i 'password|api[_-]?key|sk-|@gmail' .`  
3. Confirm no live packs or personal `registry.json` committed  

---

## Requirements

- Python **3.10+** for `hive.py` (stdlib only — no pip deps)  
- An agent host that can load markdown skills (or you run rituals by hand)  
- A filesystem (local-first by design)  

---

## Contributing / using

MIT — see [`LICENSE`](LICENSE).  

Please keep:

- examples synthetic  
- secrets out of packs  
- peer attribution honest  

PRs that bake hive into default `/recall` will be rejected unless the product law is deliberately redesigned.

---

## One-line

> Distill. Reload. When you need the crew’s filing cabinet, open the hive — labeled, budgeted, never confused with your own mind.
