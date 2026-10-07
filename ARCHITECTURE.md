# Architecture

## 1. High-Level Overview

python3-capsolver is a Python 3.8+ client library (SDK) for the Capsolver cloud captcha-solving API. It ships one package, `python3_capsolver`, distributed on PyPI, with a dual execution model: every capability exists twice — synchronous via `requests`, asynchronous via `aiohttp` (`src/python3_capsolver/core/sio_captcha_instrument.py`, `src/python3_capsolver/core/aio_captcha_instrument.py`, dependency list in `pyproject.toml`). The API base URL is a constant (`REQUEST_URL` in `src/python3_capsolver/core/const.py`); the library keeps no state beyond per-instance request payloads.

Each supported captcha family is one thin service module (ReCaptcha, Cloudflare, GeeTest, DataDome, MtCaptcha, FriendlyCaptcha, Yandex SmartCaptcha, AWS WAF, image-to-text OCR, AI vision) plus a raw-API escape hatch, `control.py`; all types are registered in `CaptchaTypeEnm` (`src/python3_capsolver/core/enum.py`).

The architecture is a four-layer library with one-way dependencies: thin service classes → shared base class → HTTP instruments → support layer (schemas, enums, constants). There is no server, CLI, database, or background worker. The test suite is a live integration suite against the real Capsolver API, gated on the `API_KEY` secret (`tests/conftest.py`, `.github/workflows/test.yml`). The toolchain is `uv` (`uv.lock`, `Makefile`).

Evidence anchors: `pyproject.toml`, `src/python3_capsolver/core/base.py`, `src/python3_capsolver/core/const.py`, `src/python3_capsolver/core/enum.py`, `src/python3_capsolver/control.py`, `tests/conftest.py`.

No material unknowns: the entire runtime surface is plain importable source with no generated or vendored code.

## 2. System Architecture (Logical)

```
Service     (recaptcha.py, cloudflare.py, control.py, ...)
   │  inherits CaptchaParams   (control.py also calls instruments directly)
   ▼
Base        (core/base.py — CaptchaParams)
   │  instantiates per-call instruments
   ▼
Instrument  (core/sio_captcha_instrument.py, core/aio_captcha_instrument.py,
   │         core/captcha_instrument.py)
   ▼
Support     (core/serializer.py, core/enum.py, core/const.py,
             core/utils.py, core/context_instr.py)
```

### Service layer (captcha facades)

- Responsibility: define per-captcha-type constructor parameters; expose solving entry points to users.
- Code locations: `src/python3_capsolver/*.py` — one module per captcha family.
- Entry points: public classes such as `ReCaptcha` (`src/python3_capsolver/recaptcha.py`) and `Control` (`src/python3_capsolver/control.py`); the solving methods `captcha_handler()` / `aio_captcha_handler()` are inherited from the base, not redefined per service.
- Depends on: base layer (`core/base.py`) and support enums (`core/enum.py`); `control.py` additionally imports both instruments directly.
- Must not depend on: `requests`, `aiohttp`, or any HTTP library.
- Owns: captcha-type-specific task parameter names only.
- State and external boundaries: none — pure parameter holders.
- Evidence: import blocks of all `src/python3_capsolver/*.py` (none import an HTTP library; only `control.py` imports instruments).

### Base layer (CaptchaParams)

- Responsibility: merge service constructor arguments with per-call `task_payload`; dispatch to the sync or async instrument; provide `with` / `async with` support.
- Code locations: `src/python3_capsolver/core/base.py`.
- Entry points: `CaptchaParams.captcha_handler()`, `CaptchaParams.aio_captcha_handler()`.
- Depends on: instrument layer and support layer (`serializer.py`, `enum.py`, `const.py`, `context_instr.py`, `captcha_instrument.py`).
- Must not depend on: any service module — nothing in `core/` imports from the package root.
- Owns: the mutable request payloads (`create_task_payload`, `get_result_params`, `task_params`) that instruments read.
- State and external boundaries: holds user credentials (`clientKey`) in memory; performs no I/O of its own.
- Evidence: `core/base.py` imports; `class CaptchaParams(SIOContextManager, AIOContextManager)`.

### Instrument layer (HTTP execution)

- Responsibility: all network I/O — build requests from msgspec structs, mount retry adapters, run the create-then-poll cycle; prepare image files (base64-encode local files, download from URLs).
- Code locations: `src/python3_capsolver/core/sio_captcha_instrument.py` (sync, `requests`), `src/python3_capsolver/core/aio_captcha_instrument.py` (async, `aiohttp`), `src/python3_capsolver/core/captcha_instrument.py` (`CaptchaInstrumentBase` plus `FileInstrument`).
- Entry points: `SIOCaptchaInstrument.processing_captcha()`, `AIOCaptchaInstrument.processing_captcha()`, static `send_post_request()` (the path `control.py` uses), `FileInstrument.file_processing()` / `aio_file_processing()` (called directly by consumers, per docstring examples).
- Depends on: support layer only (`serializer.py`, `enum.py`, `const.py`, `utils.py`).
- Must not depend on: base or service modules — instruments receive a `captcha_params` instance per call but import nothing from above their layer.
- Owns: HTTP sessions, retry-adapter wiring, the polling loop and its attempt budget.
- State and external boundaries: the only code that talks to `https://api.capsolver.com`; may read local files and fetch image URLs for file-based tasks.
- Evidence: import blocks of the three instrument files; `RETRIES` mounted on `requests.Session` in `sio_captcha_instrument.py`.

### Support layer (contracts and constants)

- Responsibility: API request/response schemas, enums, constants, retry-policy objects, context-manager mixins, attempt generator.
- Code locations: `src/python3_capsolver/core/serializer.py`, `core/enum.py`, `core/const.py`, `core/utils.py`, `core/context_instr.py`.
- Entry points: not applicable — consumed by upper layers.
- Depends on: stdlib plus `msgspec`, `tenacity`, `requests.adapters` (retry-policy objects only).
- Must not depend on: base, instrument, or service layers.
- Owns: `msgspec.Struct` request/response models with `to_dict()`; `CaptchaTypeEnm`; `REQUEST_URL`, `RETRIES`, `ASYNC_RETRIES`, `VALID_STATUS_CODES`.
- State and external boundaries: none; disables urllib3 warnings at import time (`const.py`).
- Evidence: import blocks of the five support modules — all comply.

## 3. Code Map (Physical)

```
.
├── src/python3_capsolver/            # the shipped package (setuptools src layout)
│   ├── core/                         # base + instruments + support (see §2)
│   │   ├── base.py                   # CaptchaParams — shared dispatcher
│   │   ├── captcha_instrument.py     # CaptchaInstrumentBase + FileInstrument
│   │   ├── sio_captcha_instrument.py # sync HTTP + create-then-poll loop
│   │   ├── aio_captcha_instrument.py # async HTTP + create-then-poll loop
│   │   └── serializer.py, enum.py, const.py, utils.py, context_instr.py
│   ├── control.py                    # raw API access: get_balance, create_task, get_task_result
│   ├── recaptcha.py, cloudflare.py, gee_test.py, datadome_slider.py,
│   │   mt_captcha.py, friendly_captcha.py, yandex.py, aws_waf.py,
│   │   image_to_text.py, vision_engine.py      # one facade per captcha family
│   └── __init__.py                   # exports __version__ only; full-path imports by design
├── tests/                            # live integration suite, one file per service
│   ├── conftest.py                   # BaseTest (reads API_KEY env), delay fixtures
│   └── files/                        # captcha images for file-based tests
├── docs/                             # Sphinx sources; per-module pages in docs/modules/
├── files/                            # images referenced by README and docs
├── pyproject.toml, uv.lock           # build, dependencies, tool config (uv toolchain)
├── Makefile                          # tests, lint, refactor, build, upload, doc
└── .coveragerc                       # coverage scoped to python3_capsolver/, tests omitted
```

Where is X?

- Adding a captcha type → new module in `src/python3_capsolver/` inheriting `CaptchaParams`, plus a value in `CaptchaTypeEnm` (`core/enum.py`).
- HTTP retry and polling tuning → `core/const.py` (`RETRIES`, `ASYNC_RETRIES`) and the `attempts_generator` default in `core/utils.py`.
- API payload/response schemas → `core/serializer.py`.
- The create-then-poll loop → `__create_task` / `__get_result` in both instrument modules.
- Image/file preprocessing (base64, URL fetch) → `FileInstrument` in `core/captcha_instrument.py`, invoked at the consumer call site before results enter `task_payload`.

## 4. Life of a Request / Primary Data Flow

### Flow 1 — captcha solving (primary; sync shown, async mirrors it)

1. Trigger: consumer instantiates a facade, e.g. `ReCaptcha(api_key=..., captcha_type=CaptchaTypeEnm.ReCaptchaV2TaskProxyLess)`, then calls `captcha_handler(task_payload={...})` (or `aio_captcha_handler()`).
2. Entry point: `CaptchaParams.captcha_handler()` in `src/python3_capsolver/core/base.py`.
3. Coordination: `CaptchaParams` merges `task_payload` into `self.task_params` and instantiates `SIOCaptchaInstrument(self)` (`AIOCaptchaInstrument` for async).
4. Core or domain processing: `processing_captcha()` builds a `RequestCreateTaskSer` struct and POSTs to `/createTask`; if the task is not immediately ready, it sleeps `sleep_time` and polls `/getTaskResult` up to 15 times (`attempts_generator()` yields 1..15), returning on status `ready` or `failed`, or a synthesized failure response on exhaustion.
5. Persistence or external interaction: the only external system is the Capsolver API at `REQUEST_URL` (`core/const.py`); there is no local persistence.
6. Output or side effect: a `dict` with the full API response, including the solution.

Architectural boundaries crossed:
- Service → Base → Instrument → Support; the result crosses back up as plain dicts.

Evidence:
- `src/python3_capsolver/core/base.py`
- `src/python3_capsolver/core/sio_captcha_instrument.py`
- `src/python3_capsolver/core/aio_captcha_instrument.py`
- `src/python3_capsolver/core/utils.py`

### Flow 2 — raw API call via Control (sanctioned bypass)

1. Trigger: consumer calls e.g. `Control(api_key=...).get_balance()` or `aio_get_balance()`.
2. Entry point: `Control` methods in `src/python3_capsolver/control.py`.
3. Coordination: none — `Control` skips the payload-merge and polling abstraction and invokes instruments directly.
4. Core or domain processing: one-shot `SIOCaptchaInstrument.send_post_request()` / `AIOCaptchaInstrument.send_post_request()` targeting an `EndpointPostfixEnm` endpoint; `create_task()` / `get_task_result()` accept hand-built task payloads without the solving-loop "sugar".
5. Persistence or external interaction: same single Capsolver API boundary.
6. Output or side effect: raw API response `dict`.

Architectural boundaries crossed:
- Service → Instrument directly — the one sanctioned exception to "services never touch instruments".

Evidence:
- `src/python3_capsolver/control.py`

## 5. Architectural Invariants & Constraints

- Rule: dependency direction is one-way — Service → Base → Instrument → Support.
  - Rationale: keeps HTTP details out of facades and keeps the support layer reusable without cycles.
  - Enforcement / Signals: convention, verified by import inspection; no import-linter or architecture test exists. CI lint (`.github/workflows/lint.yml`, `make lint`) checks formatting only (autoflake, black, isort).
- Rule: service modules must not import `requests` or `aiohttp`.
  - Rationale: all HTTP lives in the instrument layer.
  - Enforcement / Signals: convention plus review; the import block of every service module complies today.
- Rule: every capability ships in both sync and async form.
  - Rationale: dual-mode operation is the library's core offering (`Framework :: AsyncIO` classifier in `pyproject.toml`).
  - Enforcement / Signals: paired classes and methods (`SIOCaptchaInstrument` / `AIOCaptchaInstrument`, `file_processing` / `aio_file_processing`, `SIOContextManager` / `AIOContextManager`) and paired tests (`tests/test_sio_captcha_instrument.py`, `tests/test_aio_captcha_instrument.py`).
- Rule: all API serialization uses `msgspec.Struct` subclasses with `to_dict()`; the `json` module is never imported in `src/`.
  - Rationale: a single typed serialization path for all API contracts.
  - Enforcement / Signals: `core/serializer.py` is the only schema home; no `json` import exists anywhere in `src/`.
- Rule: new captcha types must be registered in `CaptchaTypeEnm`.
  - Rationale: `CaptchaParams.__init__` builds `TaskSer(type=captcha_type.value)` from the enum, so dispatch depends on it.
  - Enforcement / Signals: runtime failure for unregistered types; `core/base.py` constructor; change rules in `src/python3_capsolver/AGENTS.md`.
- Rule: retry and polling budgets are centralized in `core/const.py` and `core/utils.py`, not per-instrument literals.
  - Rationale: a single point of change covering both execution modes.
  - Enforcement / Signals: `RETRIES`, `ASYNC_RETRIES`, `VALID_STATUS_CODES` in `const.py`; consumed by `sio_captcha_instrument.py` and `captcha_instrument.py`; `attempts_generator` in `utils.py` drives the poll loop.
- Rule: package `__init__.py` files stay minimal (root exports only `__version__`); users import via full module paths.
  - Rationale: explicit imports with no facade namespace or re-export cycles.
  - Enforcement / Signals: `src/python3_capsolver/__init__.py` and `core/__init__.py` contents; all docstring examples use full-path imports.
- Rule: source must remain Python 3.8-compatible.
  - Rationale: the declared support floor.
  - Enforcement / Signals: `requires-python = ">=3.8"` and 3.8–3.14 classifiers in `pyproject.toml`; 3.8–3.14 matrix in `.github/workflows/build.yml` and `install.yml`.
- Rule: tests are live integration tests gated on `API_KEY`, with rate-limiting delays.
  - Rationale: the suite exercises the real Capsolver API; delays prevent throttling.
  - Enforcement / Signals: `tests/conftest.py` (`BaseTest.API_KEY = os.environ["API_KEY"]`, `delay_func` 1 s per function, `delay_class` 2 s per class); `.github/workflows/test.yml` injects the secret and runs `make tests` on Python 3.12.
- Rule: repo-only instruction documents must not ship in the wheel.
  - Rationale: `AGENTS.md` files are contributor tooling, not user documentation.
  - Enforcement / Signals: `MANIFEST.in` includes only `README.md` and `LICENSE`.

## 6. Documentation Strategy

`ARCHITECTURE.md` (this file) owns the global architecture map: layers, dependency direction, code map, representative flows, and invariants.

- `AGENTS.md` (root) — repository-wide operating rules, validation commands, and context routing to the child files below.
- `src/python3_capsolver/AGENTS.md` — service-layer conventions and per-service change rules.
- `src/python3_capsolver/core/AGENTS.md` — core module internals and safe-change guidance.
- `tests/AGENTS.md` — test patterns, fixtures, and how to add tests for new services.
- `README.md` (and `README.es-ES.md`) — user-facing usage and installation.
- `docs/` — Sphinx API reference built with `make doc` (CI: `.github/workflows/build_sphinx.yml`); one page per module under `docs/modules/`.

No ADRs, runbooks, or `DESIGN.md` exist in the repository; for a single-package library of this size their absence does not limit architectural understanding.
