# Architecture

## 1. High-Level Overview

python3-capsolver is a Python 3.8+ client library for the [Capsolver](https://capsolver.com) captcha-solving API (`Observed`: `pyproject.toml` lines 38–43, `src/python3_capsolver/core/const.py` line 18). It provides a unified interface for submitting captcha tasks to Capsolver's cloud service and polling for results, covering ReCaptcha, Cloudflare Turnstile, GeeTest, DataDome, AWS WAF, MtCaptcha, FriendlyCaptcha, Yandex SmartCaptcha, image-to-text OCR, and AI vision tasks (`Observed`: `src/python3_capsolver/core/enum.py` `CaptchaTypeEnm`, service files in `src/python3_capsolver/`).

The library is a single-package SDK distributed via PyPI as `python3-capsolver`. It exposes a dual sync/async API — synchronous calls use `requests`, asynchronous calls use `aiohttp` — so consumers can integrate it into either threading or `asyncio` applications without switching libraries (`Observed`: `pyproject.toml` lines 86–91, `core/sio_captcha_instrument.py` imports `requests`, `core/aio_captcha_instrument.py` imports `aiohttp`).

Architecturally the codebase is a layered library: thin per-captcha-type service classes at the top, a shared base class that merges payloads and delegates to HTTP instruments, and a support layer of serializers, enums, and constants at the bottom. There is no server, no CLI, and no database — the library is a pure API client.

Evidence anchors: `pyproject.toml`, `src/python3_capsolver/core/base.py`, `src/python3_capsolver/core/enum.py`, `src/python3_capsolver/core/const.py`, `src/python3_capsolver/recaptcha.py`, `src/python3_capsolver/core/serializer.py`.

## 2. System Architecture (Logical)

Four layers with strict top-to-bottom dependency direction:

```
┌─────────────────────────────────────────────┐
│  Service layer                               │
│  (recaptcha.py, cloudflare.py, control.py,   │
│   gee_test.py, aws_waf.py, ...)              │
│  Thin wrappers: __init__ only, zero HTTP      │
└──────────────────┬──────────────────────────┘
                   │ inherits CaptchaParams
                   ▼
┌─────────────────────────────────────────────┐
│  Base layer                                  │
│  (core/base.py: CaptchaParams)               │
│  Merges task payloads, delegates to           │
│  sync/async instruments                       │
└──────────────────┬──────────────────────────┘
                   │ creates instrument instances
                   ▼
┌─────────────────────────────────────────────┐
│  Instrument layer                            │
│  (core/sio_captcha_instrument.py — sync,     │
│   core/aio_captcha_instrument.py — async,    │
│   core/captcha_instrument.py — base + files)  │
│  All HTTP, retries, and result-polling        │
└──────────────────┬──────────────────────────┘
                   │ uses
                   ▼
┌─────────────────────────────────────────────┐
│  Support layer                               │
│  (core/serializer.py — msgspec.Struct,       │
│   core/enum.py — CaptchaTypeEnm etc.,        │
│   core/const.py — URLs, retry config,        │
│   core/context_instr.py — context managers,   │
│   core/utils.py — attempt generator)          │
└─────────────────────────────────────────────┘
```

**Dependency direction:** Service → Base → Instrument → Support. Never upward (`Observed`: import graph in all source files follows this direction; no lower layer imports from an upper layer).

**What each layer does NOT depend on:**

- **Service layer** never imports `requests`, `aiohttp`, or any HTTP library directly (`Observed`: all service files import only from `core.base` and `core.enum`).
- **Base layer** never performs HTTP calls itself — it delegates to instrument instances (`Observed`: `core/base.py` has no HTTP imports).
- **Support layer** never depends on service, base, or instrument layers (`Observed`: `serializer.py`, `enum.py`, `const.py`, `utils.py`, `context_instr.py` import only stdlib and `msgspec`/`tenacity`).

**Key boundary:** `control.py` is architecturally distinct from the other service files. It bypasses the create-then-poll abstraction and calls instrument methods directly (`get_balance`, `create_task`, `get_task_result`) (`Observed`: `control.py` imports `AIOCaptchaInstrument` and `SIOCaptchaInstrument` directly, unlike other services which rely solely on `CaptchaParams.captcha_handler()` / `aio_captcha_handler()`).

## 3. Code Map (Physical)

```
.
├── src/python3_capsolver/          # Library source (setuptools package root)
│   ├── core/                       # Shared infrastructure
│   │   ├── base.py                 # CaptchaParams — base class all services inherit
│   │   ├── captcha_instrument.py   # CaptchaInstrumentBase (abstract) + FileInstrument
│   │   ├── sio_captcha_instrument.py  # Sync instrument: requests-based HTTP + polling
│   │   ├── aio_captcha_instrument.py  # Async instrument: aiohttp-based HTTP + polling
│   │   ├── serializer.py           # msgspec.Struct request/response models
│   │   ├── enum.py                 # CaptchaTypeEnm, ResponseStatusEnm, EndpointPostfixEnm
│   │   ├── const.py                # REQUEST_URL, RETRIES, ASYNC_RETRIES, APP_ID
│   │   ├── context_instr.py        # SIOContextManager, AIOContextManager mixins
│   │   └── utils.py                # attempts_generator (retry loop control)
│   ├── control.py                  # Raw API access (balance, create_task, get_task_result)
│   ├── recaptcha.py                # ReCaptcha V2/V3/Enterprise solver
│   ├── cloudflare.py               # Cloudflare Turnstile/Challenge solver
│   ├── gee_test.py                 # GeeTest V3/V4 solver
│   ├── datadome_slider.py          # DataDome slider solver
│   ├── mt_captcha.py               # MtCaptcha solver
│   ├── aws_waf.py                  # AWS WAF bypass solver
│   ├── friendly_captcha.py         # FriendlyCaptcha solver
│   ├── yandex.py                   # Yandex SmartCaptcha solver
│   ├── image_to_text.py            # OCR image-to-text solver
│   ├── vision_engine.py            # AI vision engine solver
│   ├── __init__.py                 # Exports __version__ only — no re-exports
│   └── __version__.py              # Version string
│
├── tests/                          # Pytest integration test suite (mirrors src/ layout)
│   ├── conftest.py                 # BaseTest class, rate-limiting fixtures
│   ├── files/                      # Test assets (captcha images)
│   └── test_*.py                   # One test file per service + test_core + test_instrument
│
├── docs/                           # Sphinx documentation source
├── pyproject.toml                  # Build config, dependencies, tool settings
├── Makefile                        # make tests, refactor, lint, build, doc
└── .coveragerc                     # Coverage: measures python3_capsolver/ only
```

**Where is X?**

- A new captcha type → create a file in `src/python3_capsolver/`, inherit `CaptchaParams`, register the type in `core/enum.py` `CaptchaTypeEnm`.
- HTTP retry configuration → `core/const.py` (`RETRIES`, `ASYNC_RETRIES`).
- API payload schemas → `core/serializer.py` (`msgspec.Struct` classes).
- The create-task → poll-result loop → `core/sio_captcha_instrument.py` (sync) and `core/aio_captcha_instrument.py` (async).
- File/image preprocessing (base64 encoding, URL download) → `core/captcha_instrument.py` `FileInstrument`.

## 4. Life of a Request / Primary Data Flow

This is a library (SDK), so the primary flow is the user calling a solver class. Typical path for a captcha-solving call:

```
1. User instantiates a service class
   from python3_capsolver.recaptcha import ReCaptcha
   solver = ReCaptcha(api_key="CAI-...", captcha_type=CaptchaTypeEnm.ReCaptchaV2TaskProxyLess)

2. User calls captcha_handler() or aio_captcha_handler() with task-specific params
   result = solver.captcha_handler(task_payload={"websiteURL": "...", "websiteKey": "..."})

3. CaptchaParams.captcha_handler() (core/base.py)
   → merges task_payload into self.task_params
   → creates SIOCaptchaInstrument(self)   [or AIOCaptchaInstrument for async]

4. SIOCaptchaInstrument.processing_captcha() (core/sio_captcha_instrument.py)
   → builds RequestCreateTaskSer payload via msgspec Struct.to_dict()
   → POSTs to https://api.capsolver.com/createTask
   → if task is immediately ready: returns response
   → otherwise: enters polling loop
       → sleeps sleep_time seconds
       → POSTs to https://api.capsolver.com/getTaskResult
       → repeats up to 15 attempts (attempts_generator default)
       → returns on status "ready" or "failed"

5. Returns dict with full API response including solution
```

`control.py` follows a different, shorter path — it calls `SIOCaptchaInstrument.send_post_request()` or `AIOCaptchaInstrument.send_post_request()` directly for one-shot API calls like `get_balance`, bypassing the create-then-poll cycle (`Observed`: `control.py` lines 34–54, 49–54).

## 5. Architectural Invariants & Constraints

- **Rule:** Service files must never import `requests` or `aiohttp` directly.
  - **Rationale:** All HTTP is encapsulated in the instrument layer; services are pure parameter holders.
  - **Enforcement / Signals (Observed):** No service file (e.g. `recaptcha.py`, `cloudflare.py`) contains an HTTP library import. Violation would be visible on review.

- **Rule:** All serialization must use `msgspec.Struct` with `to_dict()`, never the `json` module directly.
  - **Rationale:** Consistent serialization and type safety across the library.
  - **Enforcement / Signals (Observed):** `core/serializer.py` defines `MyBaseModel(Struct)` with `to_dict()`. All instruments call `.to_dict()` on structs.

- **Rule:** Every captcha service must support both sync (`captcha_handler`) and async (`aio_captcha_handler`) execution.
  - **Rationale:** The library's core value proposition is dual-mode operation.
  - **Enforcement / Signals (Observed):** Both methods are defined in `CaptchaParams` (`core/base.py`) and inherited by all service classes. Test suite includes paired sync/async tests.

- **Rule:** Every service class must support context manager protocols (`with` / `async with`).
  - **Rationale:** Resource cleanup pattern for library consumers.
  - **Enforcement / Signals (Observed):** `CaptchaParams` inherits both `SIOContextManager` and `AIOContextManager` mixins from `core/context_instr.py`.

- **Rule:** New captcha types must be registered in `CaptchaTypeEnm` (`core/enum.py`).
  - **Rationale:** Single source of truth for type dispatch; the base class uses enum values to build API payloads.
  - **Enforcement / Signals (Observed):** `core/base.py` constructs `TaskSer(type=captcha_type.value)` from the enum.

- **Rule:** Retry configuration is centralized in `core/const.py`, not hardcoded in instruments.
  - **Rationale:** Single point of change for retry behavior across sync and async paths.
  - **Enforcement / Signals (Observed):** `RETRIES` and `ASYNC_RETRIES` are defined in `const.py` and imported by both instruments and `FileInstrument`.

- **Rule:** Dependency direction is strictly top-down: Service → Base → Instrument → Support.
  - **Rationale:** Prevents circular dependencies and keeps the support layer reusable.
  - **Enforcement / Signals (Observed):** Import statements in all files respect this direction. No file in `core/` imports from a service file.

- **Rule:** `__init__.py` files are intentionally empty (or export only `__version__`); users import via full path.
  - **Rationale:** Explicit imports avoid namespace pollution and circular re-exports.
  - **Enforcement / Signals (Observed):** `src/python3_capsolver/__init__.py` exports `__version__` only; `core/__init__.py` is empty. Docstrings show full-path imports.

- **Rule:** Tests require `API_KEY` environment variable and include rate-limiting delays.
  - **Rationale:** Integration tests hit the live Capsolver API; delays prevent throttling.
  - **Enforcement / Signals (Observed):** `tests/conftest.py` reads `os.environ["API_KEY"]` and defines `delay_func` (1s) and `delay_class` (2s) fixtures.

## 6. Documentation Strategy

`ARCHITECTURE.md` (this file) is the global map of the repository: layers, dependency direction, invariants, and the code map. It answers "where is X?" and "what depends on what?".

Module-level detail lives in `AGENTS.md` files co-located with the code:
- `src/python3_capsolver/AGENTS.md` — service-layer conventions, file listing, and per-service change rules.
- `src/python3_capsolver/core/AGENTS.md` — core module internals: instrument responsibilities, serialization patterns, and safe-change guidance.
- `tests/AGENTS.md` — test patterns, fixtures, and how to add tests for new services.

API documentation is generated by Sphinx from `docs/` (`Observed`: `docs/conf.py`, `docs/Makefile`). Build with `make doc`.

Build, test, and lint commands are documented in the root `Makefile` and in `AGENTS.md` at repository root. The root `AGENTS.md` also contains a condensed version of the architecture summary and validation commands.

What belongs where:
- **Global architecture** (this file): layers, boundaries, invariants, physical layout, primary data flow.
- **Module `AGENTS.md`**: local file listing, local boundaries, and specific change rules for that module.
- **Sphinx `docs/`**: public API reference, usage examples, and user-facing guides.
