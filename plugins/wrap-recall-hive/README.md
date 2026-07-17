# Plugin: wrap-recall-hive

Claude Code plugin packaging three skills + the hive CLI.

| Skill | Role |
|-------|------|
| `wrap` | Distill session → own pack |
| `recall` | Load own pack (~30–50k) |
| `hive` | Opt-in crew search (`hive/hive.py`) |

Installed plugin root is available as `CLAUDE_PLUGIN_ROOT` (skills resolve the CLI there).

See the repository root README for full product docs and Grok install.
