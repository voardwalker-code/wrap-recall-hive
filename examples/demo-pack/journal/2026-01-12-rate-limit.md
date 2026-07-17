## Recall

Implemented per-key rate limiting using a token bucket. Borrowed the shape from an internal gateway note (attributed in code comments). Self-test passes.

## Notes

### What happened
- Token bucket + window reset
- Documented non-goals: no distributed store in v1

### Artifacts / paths
- `src/rate_limit.py`

### Open threads
- Multi-instance store later

## From the hive

### Hive consults this session
- **Focus:** token bucket prior art
- **Owners hit:** demo-b (example)

### Peer trails (attributed — not me)
- **[owner=demo-b · when=2026-01-11 · kind=recall]** They had already sketched a bucket API · source: `2026-01-11-bucket-sketch` (synthetic)

### What I take from them
- Keep the advisory forecast shape; don’t raise on soft cap
