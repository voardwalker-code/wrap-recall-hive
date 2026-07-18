# Plugin: wrap-recall-hive

Claude Code plugin packaging three skills + the hive CLI.

| Skill | Role |
|-------|------|
| `wrap` | Distill session → own pack |
| `recall` | Load own pack (~30–50k) |
| `hive` | Opt-in crew search (`hive/hive.py`) |

Installed plugin root is available as `CLAUDE_PLUGIN_ROOT` (skills resolve the CLI there).

## One surface (M17)

- This plugin is the **Claude marketplace** distribution path. Skills may appear as `wrap-recall-hive:…` in some UIs; natural language `wrap` / `recall` / `hive` still works.
- **Do not** also install user copies under `~/.claude/skills/{wrap,recall,hive}` — pick plugin *or* user skills.
- **Grok Build:** do **not** use this as a daily Grok plugin. Grok namespaces plugin skills and doubles the UI if loose skills are also present. Grok seats use `./scripts/install-grok.sh` → plain names in `~/.grok/skills/`.

See the repository root README and [`docs/INSTALL.md`](../../docs/INSTALL.md).
