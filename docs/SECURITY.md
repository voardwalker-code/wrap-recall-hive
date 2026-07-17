# Security & privacy

## Private by default (this repo)

If the GitHub repository is **private**, treat that as a review gate before any public flip:

1. Search the tree for personal paths, emails, hostnames, API keys, family names, private project codenames you do not want public.  
2. Confirm `hive/registry.json` is **not** committed (only `registry.example.json` + `examples/demo-registry.json`).  
3. Confirm no live `~/.…/memory` journals were copied into the package.  
4. Run: `rg -i 'password|api[_-]?key|sk-|BEGIN RSA|@gmail\.com' .` (or equivalent).  

## What never belongs in a pack

- API keys, OAuth tokens, `auth.json`, `.env`  
- Private chat transcripts wholesale  
- Unredacted customer data  
- Other people’s private packs  

## What is OK in a pack (still sensitive)

- Project paths on your machine  
- Working agreements with a human  
- Scar journals about failures  

**Recommendation:** keep live packs outside git; only ship skills, CLI, examples, and docs in this repository.

## Hive is read-only

`hive.py` does not write packs. Compromise of the CLI should not mutate memory roots. Still: a malicious registry can *point* at sensitive files for *read* — only register roots you accept sharing with the active seat.
