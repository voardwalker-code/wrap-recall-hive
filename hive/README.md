# Hive CLI

Seat-neutral, **read-only** search over registered memory packs and shared house files.

```bash
# From this directory (after copying registry.example.json → registry.json)
python3 hive.py --list-owners
python3 hive.py --focus "auth refactor"
python3 hive.py --focus "deploy" --from agent-b
python3 hive.py --focus "rate limit" --budget-chars 80000
```

## Files

| File | Role |
|------|------|
| `hive.py` | Stdlib-only CLI (Python 3.10+) |
| `registry.example.json` | Template owner → path map |
| `registry.json` | Your local map (**gitignored** pattern in package root) |

## Environment

| Var | Effect |
|-----|--------|
| `HIVE_REGISTRY` | Absolute path to a registry JSON file |

## Output contract

Every span is wrapped:

```markdown
### [memory owner=agent-b kind=recall when=2026-01-15 status=done not_me=true]
<source>/path/to/journal/….md</source>
…
```

Assembly ends with a **Hive report** (hits taken, dropped, owners, paths).

## Laws

- Read-only — never writes packs  
- Budget default ~120k chars (~30k tokens); ceiling 200k  
- Skips obvious credential filenames  
- Does not replace `/wrap` or `/recall`  
