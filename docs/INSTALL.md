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

Grok has its **own** plugin + marketplace system (`/plugins`, `/marketplace`, `grok plugin …`).  
It also discovers loose skills under `~/.grok/skills/` (and Claude’s skills for compat).

### A. Plugin install (recommended — same public repo)

```bash
grok plugin install voardwalker-code/wrap-recall-hive --trust
grok plugin enable wrap-recall-hive   # if not already enabled
```

TUI: `/plugins` → **a** add `voardwalker-code/wrap-recall-hive` → enable,  
or `/marketplace` → add source → install.

Hive CLI resolves via `GROK_PLUGIN_ROOT` (plugin root includes `hive/hive.py`).

Optional: install only the Claude-shaped subtree:

```bash
grok plugin install 'voardwalker-code/wrap-recall-hive#plugins/wrap-recall-hive' --trust
```

### B. Marketplace source

```bash
grok plugin marketplace add voardwalker-code/wrap-recall-hive
grok plugin marketplace list
grok plugin install voardwalker-code/wrap-recall-hive --trust
```

### C. Loose skills script (no plugin manager)

```bash
git clone https://github.com/voardwalker-code/wrap-recall-hive.git
cd wrap-recall-hive
./scripts/install-grok.sh
```

→ skills in `~/.grok/skills/` + CLI in `~/.local/share/wrap-recall-hive/`.

### D. Config path (dev)

```toml
# ~/.grok/config.toml
[skills]
paths = ["~/Projects/wrap-recall-hive/skills"]

[plugins]
paths = ["~/Projects/wrap-recall-hive"]
```

### Both hosts at once

```bash
./scripts/install.sh
grok plugin install voardwalker-code/wrap-recall-hive --trust
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
