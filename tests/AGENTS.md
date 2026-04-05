# AGENTS.md

## Scope

Pytest integration test suite. Tests call the live Capsolver API and require `API_KEY` in the environment.

## What lives here

```text
tests/
├── conftest.py               # BaseTest class, rate-limiting fixtures
├── test_core.py              # CaptchaParams, enums, context managers
├── test_instrument.py        # FileInstrument, CaptchaInstrumentBase
├── test_control.py           # Control: get_balance, create_task, get_task_result
├── test_recaptcha.py         # ReCaptcha V2/V3/Enterprise
├── test_cloudflare.py        # Cloudflare Turnstile/Challenge
├── test_*.py                 # One file per captcha service
└── files/                    # Test assets (captcha_example.jpeg)
```

## Local boundaries and invariants

- All test classes inherit `BaseTest` from `conftest.py` — provides `API_KEY`, `sleep_time`, `get_random_string()`, `read_image()`
- Every sync test (`def test_*`) has a corresponding async test (`async def test_aio_*`)
- Rate-limiting fixtures are mandatory: `delay_func` (1s, function scope) and `delay_class` (2s, class scope) prevent API throttling
- Tests are integration tests against the live API — they will fail without a valid `API_KEY` env var
- `pytest-asyncio` runs in `auto` mode (configured in `pyproject.toml`)

## Safe change rules

- When adding a new captcha service, create a matching `test_<service>.py` inheriting `BaseTest` with both sync and async test methods
- Do not remove or reduce rate-limiting fixtures — the API will throttle without them
- Coverage is configured in `.coveragerc`: measures `python3_capsolver/` only, omits `tests/`
- Run specific tests with `uv run pytest tests/ -k <name>`, full suite with `make tests`
