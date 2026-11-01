# test — service toolkit with an open bug backlog

A small Python service (FastAPI auth endpoints) plus a toolkit of utility modules. It is the
target repository for **AgentOps**: every open GitHub issue describes one real bug, reproduced
by exactly one failing test, so each issue can be investigated, fixed and shipped as its own PR.

## Layout

| Module | What it does |
| --- | --- |
| `app/main.py` | Auth service: `/health`, `/login`, `/users/me` |
| `app/text.py` | Slugs, truncation, casing, masking |
| `app/numbers.py` | Rounding, statistics, number theory |
| `app/collections_utils.py` | Chunking, grouping, merging collections |
| `app/dates.py` | Calendar math, business days, durations |
| `app/validators.py` | Email, URL, phone, card and ID validation |
| `app/pricing.py` | Discounts, tax, shipping, loans (Decimal money) |
| `app/inventory.py` | Stock levels, reservations, FIFO allocation |
| `app/search.py` | Pagination, sorting, filtering, search |
| `app/security.py` | Sanitizing, hashing, tokens, rate limiting |
| `app/parsing.py` | CSV, query strings, sizes, versions, numerals |

Every function documents its contract in its docstring; tests in `tests/test_<module>.py`
have one test per function (`test_<function>`).

## Running tests

```bash
pip install -r requirements.txt
pytest                                   # whole suite
pytest tests/test_text.py::test_slugify  # one issue's test
```

The suite is expected to fail until the backlog is cleared: each open issue names the test
that reproduces it. A fix for an issue should make its test pass without breaking any other
test.
