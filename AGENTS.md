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
│   └── test_*.py                 # Per-service tests + core/instrument/control tests
├── docs/                         # Sphinx documentation (make doc); module pages in docs/modules/
├── files/                        # Images used by README and docs
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

## Context routing

Read only when relevant:

- Architectural or cross-module changes → `ARCHITECTURE.md` (full system map, request/data flow, invariants)
- Editing service classes or adding a captcha type → `src/python3_capsolver/AGENTS.md`
- Editing instruments, serializers, enums, or constants → `src/python3_capsolver/core/AGENTS.md`
- Adding or modifying tests → `tests/AGENTS.md`
- Sphinx docs changes → `docs/` (built with `make doc`; one page per module under `docs/modules/`)

## Change rules

- Every new captcha service must inherit `CaptchaParams`, provide `captcha_handler()` + `aio_captcha_handler()`, and register its type in `CaptchaTypeEnm`
- All serialization must use `msgspec.Struct` — never raw `json` module
- Dual sync/async is mandatory for any new instrument or service
- Service classes are thin: only `__init__` with captcha-type-specific params; all HTTP goes through instruments
- Context manager support (`with` / `async with`) is required on all service classes
- Keep syntax Python 3.8-compatible — CI runs a 3.8–3.14 matrix (`.github/workflows/build.yml`)

## Validation

```bash
make tests                       # pytest + coverage (HTML + XML) — same as CI (test.yml)
make lint                        # autoflake --check, black --check, isort --check-only — same as CI (lint.yml)
make refactor                    # autoflake + black + isort on src/ and tests/
uv run pytest tests/ -k <name>   # run specific tests
```

Tests require the `API_KEY` environment variable and call the live Capsolver API. Rate-limiting fixtures (`delay_func` 1s, `delay_class` 2s) prevent API throttling.

## Repository-specific gotchas

- **Empty `__init__.py` files**: users import via full path (`from python3_capsolver.recaptcha import ReCaptcha`), never from top-level package
- **`AGENTS.md` files are repo-only**: they do not ship in the wheel — `MANIFEST.in` includes only `README.md` + `LICENSE` (verified against built wheels in `dist/`). Keep the tree at exactly two files inside `src/` (package root and `core/`); do not add deeper ones or packaging rules that would include them
- **`control.py` is the largest file** (431 lines) and provides direct API access without the captcha-handling abstraction
- **Toolchain is `uv`**: use `uv run`, `uv sync`, `uv build` — not bare `pip` or `pytest`
- **`captcha_instrument.py` is 221 lines**: contains both `CaptchaInstrumentBase` and `FileInstrument`; edits here affect all services
