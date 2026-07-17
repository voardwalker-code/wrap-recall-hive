# Install guide — Claude Code & Grok Build

## What gets installed

| Piece | Purpose |
|-------|---------|
| Skills `wrap`, `recall`, `hive` | Ritual procedures agents load on cue |
| `hive/hive.py` + registry example | Seat-neutral crew search CLI |
| Optional pack templates | Under `pack/` (copy by hand into your pack root) |

**Live personal packs are never installed from this repo.** You create those separately.

---

## Claude Code

### A. Plugin marketplace (recommended for distribution)

When the repo is available to Claude (local path or **public** GitHub):

**Local test (private ok):**

```text
/plugin marketplace add /absolute/path/to/wrap-recall-hive
/plugin install wrap-recall-hive@wrap-recall-hive
```

**After public:**

```text
/plugin marketplace add voardwalker-code/wrap-recall-hive
/plugin install wrap-recall-hive@wrap-recall-hive
```

CLI equivalent:

```bash
claude plugin marketplace add /path/to/wrap-recall-hive
claude plugin install wrap-recall-hive@wrap-recall-hive
claude plugin validate /path/to/wrap-recall-hive
```

Plugin skills may appear **namespaced** (e.g. `wrap-recall-hive:wrap`). Natural language cues (`wrap`, `hive`) still match skill descriptions.

Hive CLI inside the plugin resolves via `CLAUDE_PLUGIN_ROOT`.

### B. User skills (simple, same as many personal skills)

```bash
./scripts/install.sh --claude
# or: ./scripts/install.sh --claude --link   # symlink to this clone for dev
```

Copies (or links) into `~/.claude/skills/{wrap,recall,hive}/` and installs the CLI under:

`~/.local/share/wrap-recall-hive/` (override with `--home` or `WRAP_RECALL_HIVE_HOME`).

### C. Project-scoped skills

```bash
mkdir -p .claude/skills
cp -R skills/* .claude/skills/
# hive still needs WRAP_RECALL_HIVE_HOME or a local copy of hive/
```

---

## Grok Build

Grok does **not** use Claude’s `/plugin` marketplace. It discovers skills from disk:

| Location | Scope |
|----------|--------|
| `~/.grok/skills/` | User (all projects) |
| `<repo>/.grok/skills/` | That repo |
| `~/.claude/skills/` | Also scanned by default (Claude compat) |

### Recommended install

```bash
git clone https://github.com/voardwalker-code/wrap-recall-hive.git   # or local path
cd wrap-recall-hive
./scripts/install-grok.sh
# dev: ./scripts/install-grok.sh --link
```

This:

1. Installs hive CLI → `~/.local/share/wrap-recall-hive/hive/`  
2. Installs skills → `~/.grok/skills/{wrap,recall,hive}/`  
3. Writes `env.sh` with `WRAP_RECALL_HIVE_HOME`

Optional: `source ~/.local/share/wrap-recall-hive/env.sh` in your shell profile.

### Config alternative (no copy)

Point Grok at a skills directory without copying:

```toml
# ~/.grok/config.toml
[skills]
paths = ["~/Projects/wrap-recall-hive/skills"]
```

Still install the hive CLI data home (or keep using the clone path in the hive skill resolution list).

### Both hosts at once

```bash
./scripts/install.sh          # Grok + Claude user skills
./scripts/install.sh --link   # symlink skills to this repo
```

---

## Own pack (both hosts)

```bash
mkdir -p ~/.agent-memory/primary/{journal,worklog}
cp pack/relationship-spine.example.md ~/.agent-memory/primary/relationship-spine.md
```

Or use host-native roots:

- Grok often: `~/.grok/memory/`  
- Claude often: `~/.claude/claude-memory/`  

Edit skill/pack docs to match the root you actually use.

### Multi-seat hive

```bash
cp ~/.local/share/wrap-recall-hive/hive/registry.example.json \
   ~/.local/share/wrap-recall-hive/hive/registry.json
# edit owner roots
python3 ~/.local/share/wrap-recall-hive/hive/hive.py --list-owners
```

---

## Verify

```bash
python3 "${WRAP_RECALL_HIVE_HOME:-$HOME/.local/share/wrap-recall-hive}/hive/hive.py" \
  --registry examples/demo-registry.json --focus "rate limit"
```

(From a clone, you can also use `./hive/hive.py --registry examples/demo-registry.json`.)

In-session:

- Claude / Grok: say `wrap`, `recall`, or `hive <focus>`  
- Claude plugin: `/plugin` list should show `wrap-recall-hive`  

---

## Private repo note

`/plugin marketplace add owner/repo` over GitHub needs clone access. **Private** remotes work if git credentials/SSH are set; for public distribution, flip the repo public after `docs/SECURITY.md`.

Local path add always works for dogfood:

```text
/plugin marketplace add /home/you/Projects/wrap-recall-hive
```
