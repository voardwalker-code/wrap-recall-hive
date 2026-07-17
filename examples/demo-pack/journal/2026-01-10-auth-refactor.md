## Recall

Refactored token validation into a pure function. Added unit tests for expired and malformed tokens.
Left rate-limit integration as an open thread.

## Notes

### What happened
- Extracted `validate_token`
- Tests cover happy path + two failures

### Artifacts / paths
- `src/auth/tokens.py`
- `tests/test_tokens.py`

### Open threads
- Wire rate limiter from gateway prior art

## From the hive

_No hive consult this session._
