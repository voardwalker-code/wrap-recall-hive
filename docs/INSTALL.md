# Install guide — Claude Code & Grok Build

## Product law: one surface (M17)

The rituals must stay **simple**:

```text
wrap · recall · hive
```

Not a second, package-prefixed twin:

```text
wrap-recall-hive:wrap · wrap-recall-hive:recall · wrap-recall-hive:hive
```

| Rule | Why |
|------|-----|
| **One install path per host** | Plugin + loose skills = two UIs for the same ritual |
| **Grok = loose skills only** | Grok plugins namespace skills as `plugin:skill` — that breaks the simplicity that made this good |
| **Claude = plugin *or* user skills** | Marketplace is fine for distribution; user skills keep plain names — **never both** |
| **Same pack either way** | Skills only change *how they appear*; your memory root does not fork |

---

## What gets installed

| Piece | Purpose |
|-------|---------|
| Skills `wrap`, `recall`, `hive` | Ritual procedures agents load on cue |
| `hive/hive.py` + registry example | Seat-neutral crew search CLI |
| Optional pack templates | Under `pack/` (copy by hand into your pack root) |

**Live personal packs are never installed from this repo.** You create those separately.

---

## Grok Build (recommended path)

**Use the install script.** Do **not** `grok plugin install` this package if you want plain `/wrap` `/recall` `/hive`.

```bash
git clone https://github.com/voardwalker-code/wrap-recall-hive.git
cd wrap-recall-hive
./scripts/install-grok.sh
```

What that does:

1. Copies hive CLI → `~/.local/share/wrap-recall-hive/`
2. Copies skills → `~/.grok/skills/{wrap,recall,hive}/` (**plain names**)
3. **Uninstalls** a Grok `wrap-recall-hive` plugin if one is present (avoids the double UI)

Then in Grok type: `recall` · `wrap` · `hive` — not `wrap-recall-hive:…`.

Dev symlink (edit skills in-repo):

```bash
./scripts/install-grok.sh --link
```

Keep a Grok plugin on purpose (not recommended):

```bash
./scripts/install-grok.sh --keep-plugin   # you will still get dual surfaces if both exist
```

### Why not the Grok plugin?

Grok’s plugin manager loads skills as **`wrap-recall-hive:recall`**.  
If you *also* have `~/.grok/skills/recall`, the slash menu shows **two recalls**. That was the confusion this package must not recreate.

Grok plugin install is **unsupported as a dual path** and **not recommended** for daily use. The public repo still has `plugin.json` so the tree is a valid plugin unit for hosts that need it — Grok seats should use loose skills.

### Config (dev only — one path)

```toml
# ~/.grok/config.toml — pick ONE, never both skills.paths + plugin

# Option A (preferred): loose skills already under ~/.grok/skills via install-grok.sh
# (nothing required)

# Option B: point at the clone instead of copying
[skills]
paths = ["~/Projects/wrap-recall-hive/skills"]

# Do NOT also:
# [plugins]
# paths = ["~/Projects/wrap-recall-hive"]
# enabled = ["wrap-recall-hive"]
```

---

## Claude Code

### A. Plugin marketplace (distribution path)

When the repo is available to Claude (local path or **public** GitHub):

**Local test:**

```text
/plugin marketplace add /absolute/path/to/wrap-recall-hive
/plugin install wrap-recall-hive@wrap-recall-hive
```

**Public:**

```text
/plugin marketplace add voardwalker-code/wrap-recall-hive
/plugin install wrap-recall-hive@wrap-recall-hive
```

CLI:

```bash
claude plugin marketplace add /path/to/wrap-recall-hive
claude plugin install wrap-recall-hive@wrap-recall-hive
claude plugin validate /path/to/wrap-recall-hive
```

Plugin skills **may appear namespaced** (e.g. `wrap-recall-hive:wrap`). Natural language cues (`wrap`, `hive`) still match skill descriptions.  
If you want plain names on Claude instead, use **B** and do **not** also install the plugin.

Hive CLI inside the plugin resolves via `CLAUDE_PLUGIN_ROOT`.

### B. User skills (plain names)

```bash
./scripts/install.sh --claude
# or: ./scripts/install.sh --claude --link
```

Copies (or links) into `~/.claude/skills/{wrap,recall,hive}/` and installs the CLI under  
`~/.local/share/wrap-recall-hive/` (override with `--home` or `WRAP_RECALL_HIVE_HOME`).

**If you already installed the marketplace plugin, remove user skill copies** so only one surface remains:

```bash
rm -rf ~/.claude/skills/{wrap,recall,hive}
```

### C. Project-scoped skills

```bash
mkdir -p .claude/skills
cp -R skills/* .claude/skills/
# hive still needs WRAP_RECALL_HIVE_HOME or a local copy of hive/
```

---

## Both hosts at once

```bash
./scripts/install.sh
# → plain skills under ~/.grok/skills and ~/.claude/skills + shared hive CLI
```

That is enough. **Do not** add:

```bash
# BAD on Grok — creates wrap-recall-hive:recall beside /recall
grok plugin install voardwalker-code/wrap-recall-hive --trust
```

Claude may still use the marketplace plugin **instead of** `~/.claude/skills` — pick one.

---

## Own pack (both hosts)

```bash
mkdir -p ~/.agent-memory/primary/{journal,worklog}
cp pack/relationship-spine.example.md ~/.agent-memory/primary/relationship-spine.md
```

Or use host-native roots:

- Grok often: `~/.grok/memory/`  
- Claude often: `~/.claude/claude-memory/`  

Edit skill/pack docs to match the root you actually use. Blank `/recall` loads spine + latest 1–3 Recalls + worklog (~30–50k) — not every journal at once. History stays on disk; focused `/recall <note>` pulls matching entries.

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

(From a clone: `./hive/hive.py --registry examples/demo-registry.json`.)

In-session:

| Host | Expect |
|------|--------|
| Grok | Slash / natural language: **`wrap`**, **`recall`**, **`hive`** only |
| Claude (user skills) | Same plain names |
| Claude (plugin only) | May show `wrap-recall-hive:…`; still one set — not duplicated with user skills |

**Fail if you see both** `/recall` **and** `wrap-recall-hive:recall` on the same host.

Recovery (Grok):

```bash
grok plugin uninstall wrap-recall-hive --confirm
./scripts/install-grok.sh
# restart Grok so the slash menu refreshes
```

---

## Private repo note

`/plugin marketplace add owner/repo` over GitHub needs clone access. **Private** remotes work if git credentials/SSH are set; for public distribution, flip the repo public after `docs/SECURITY.md`.

Local path add always works for dogfood:

```text
/plugin marketplace add /home/you/Projects/wrap-recall-hive
```
