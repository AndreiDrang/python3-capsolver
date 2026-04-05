# AGENTS.md

## Repository overview

Python 3.8+ client library for the Capsolver captcha-solving API. Single-package `src/` layout, dual sync (`requests`) / async (`aiohttp`) execution, `msgspec` for serialization, `tenacity` for async retries.

## Where to work

```text
./
├── src/python3_capsolver/        # Main library
│   ├── core/                     # Base classes, instruments, serializers, enums
│   ├── control.py                # Raw API: get_balance, create_task, get_task_result
│   ├── recaptcha.py              # ReCaptcha V2/V3/Enterprise
│   ├── cloudflare.py             # Cloudflare Turnstile/Challenge
│   └── *.py                      # Other captcha services (see package AGENTS.md)
├── tests/                        # Pytest suite mirroring source structure
│   ├── conftest.py               # BaseTest class, fixtures, rate-limiting delays
│   └── test_*.py                 # One file per service + test_core.py + test_instrument.py
├── docs/                         # Sphinx documentation (make html)
├── ARCHITECTURE.md               # Layered architecture, data flow, invariants
├── pyproject.toml                # Build, deps, black/isort/pytest config
└── Makefile                      # make tests, make refactor, make build, make doc
```

## Architecture and boundaries

Four layers with strict dependency direction (top → bottom only):

1. **Service layer** (`src/python3_capsolver/*.py`) — thin wrappers inheriting `CaptchaParams`, zero HTTP logic
2. **Base layer** (`core/base.py`) — `CaptchaParams` merges payloads, delegates to instruments
3. **Instrument layer** (`core/*_instrument.py`) — `SIOCaptchaInstrument` (sync) and `AIOCaptchaInstrument` (async) handle all HTTP, retries, and polling
4. **Support layer** (`core/serializer.py`, `core/enum.py`, `core/const.py`) — `msgspec.Struct` classes, enums, constants

**Forbidden**: service files importing `requests`/`aiohttp` directly; support layer depending on upper layers.

## Change rules

- Every new captcha service must inherit `CaptchaParams`, provide `captcha_handler()` + `aio_captcha_handler()`, and register its type in `CaptchaTypeEnm`
- All serialization must use `msgspec.Struct` — never raw `json` module
- Dual sync/async is mandatory for any new instrument or service
- Service classes are thin: only `__init__` with captcha-type-specific params; all HTTP goes through instruments
- Context manager support (`with` / `async with`) is required on all service classes

## Validation

```bash
make tests                       # pytest + coverage (HTML + XML)
make refactor                    # autoflake + black + isort on src/ and tests/
make lint                        # autoflake --check, black --check, isort --check-only
uv run pytest tests/ -k <name>   # run specific tests
```

Tests require the `API_KEY` environment variable. Rate-limiting fixtures (`delay_func` 1s, `delay_class` 2s) prevent API throttling.

## Key docs

- `ARCHITECTURE.md` — full system map, data flow, invariants
- `src/python3_capsolver/AGENTS.md` — service-level conventions
- `src/python3_capsolver/core/AGENTS.md` — core module internals
- `tests/AGENTS.md` — test patterns and fixtures

## Repository-specific gotchas

- **Empty `__init__.py` files**: users import via full path (`from python3_capsolver.recaptcha import ReCaptcha`), never from top-level package
- **`AGENTS.md` in package dirs**: these ship with the wheel unless excluded in `pyproject.toml` — do not add more inside `src/`
- **`control.py` is the largest file** (~431 lines) and provides direct API access without the captcha-handling abstraction
- **Toolchain is `uv`**: use `uv run`, `uv sync`, `uv build` — not bare `pip` or `pytest`
- **`captcha_instrument.py` is ~9.3k lines**: contains both `CaptchaInstrumentBase` and `FileInstrument`; edits here affect all services
