# Architecture

## 1. High-Level Overview

`python3-capsolver` is a Python 3.8+ client library for the Capsolver captcha-solving service API. It provides a unified, type-safe interface for solving various captcha types (ReCaptcha, Cloudflare Turnstile, GeeTest, DataDome, AWS WAF, etc.) through both synchronous and asynchronous execution models.

**Observed**: The library follows a layered architecture where core infrastructure (`core/`) provides base classes, serialization, and HTTP instruments, while service-specific modules (e.g., `recaptcha.py`, `cloudflare.py`) implement concrete captcha types. Dual sync/async support is achieved through separate instrument classes (`SIOCaptchaInstrument`, `AIOCaptchaInstrument`) that share a common interface.

**Evidence Anchors**:
- `pyproject.toml`: Dependencies (`requests`, `aiohttp`, `msgspec`, `tenacity`), build system (setuptools), Python >=3.8
- `src/python3_capsolver/core/base.py`: `CaptchaParams` base class with `captcha_handler()` and `aio_captcha_handler()`
- `src/python3_capsolver/core/enum.py`: Type-safe enums for captcha types, endpoints, response statuses
- `src/python3_capsolver/*.py`: Service-specific implementations (10+ captcha types)
- `README.md`: Usage examples, feature list, supported captcha types

**Inferred**: The library prioritizes performance (hence `msgspec` over `json`) and resilience (retry logic via `tenacity` and `requests.Retry`). The separation of concerns between core infrastructure and service implementations suggests an intentional design for extensibility.

**Unknown**: Whether there are any plans to support additional captcha types beyond those currently implemented.

## 2. System Architecture (Logical)

### Logical Components

The library consists of four logical layers:

1. **Service Layer** (`src/python3_capsolver/*.py`): High-level classes for each captcha type (e.g., `ReCaptcha`, `Cloudflare`, `Control`). Each class encapsulates captcha-specific parameters and provides sync/async handlers.

2. **Base Layer** (`src/python3_capsolver/core/base.py`): The `CaptchaParams` class serves as the common base for all service classes. It handles payload serialization, URL configuration, and delegates to appropriate instruments.

3. **Instrument Layer** (`src/python3_capsolver/core/*instrument.py`): HTTP client abstractions that manage API communication:
   - `CaptchaInstrumentBase`: Abstract base with retry logic and result polling
   - `SIOCaptchaInstrument`: Synchronous implementation using `requests`
   - `AIOCaptchaInstrument`: Asynchronous implementation using `aiohttp`
   - `FileInstrument`: File/URL/base64 processing utilities

4. **Support Layer** (`src/python3_capsolver/core/`): Utilities including:
   - `serializer.py`: `msgspec.Struct` classes for request/response serialization
   - `enum.py`: Type-safe enumerations
   - `const.py`: Configuration constants (API URLs, retry settings)
   - `utils.py`: Utility functions
   - `context_instr.py`: Context manager mixins for session cleanup

### Dependency Direction

```
Service Layer (recaptcha.py, cloudflare.py, ...)
    ↓
Base Layer (base.py: CaptchaParams)
    ↓
Instrument Layer (*instrument.py: HTTP clients)
    ↓
Support Layer (serializer, enum, const, utils)
    ↓
External Dependencies (requests, aiohttp, msgspec, tenacity)
```

**Allowed Dependencies**:
- Service classes → `CaptchaParams` (inheritance) + enums
- `CaptchaParams` → Instruments + serializers
- Instruments → Serializers + constants + external HTTP libraries
- Support layer → External libraries only (no internal dependencies)

**Forbidden Dependencies** (Inferred from structure):
- Support layer → Service/Base layers (would create circular dependencies)
- Instruments → Service-specific logic (violates separation of concerns)
- Service classes → Direct HTTP calls (must go through instruments)

### SSR/Hybrid Boundaries

Not applicable. This is a pure Python library with no frontend/web rendering components.

### Monorepo Status

Not applicable. Single-package repository with standard `src/` layout.

## 3. Code Map (Physical)

```
python3-capsolver/
├── src/python3_capsolver/        # Main library package
│   ├── core/                     # Core infrastructure (stable, rarely changes)
│   │   ├── base.py               # CaptchaParams base class
│   │   ├── captcha_instrument.py # Base + File instrument
│   │   ├── sio_captcha_instrument.py  # Sync HTTP client
│   │   ├── aio_captcha_instrument.py  # Async HTTP client
│   │   ├── serializer.py         # msgspec serialization
│   │   ├── enum.py               # Type-safe enums
│   │   ├── const.py              # Constants
│   │   └── utils.py              # Utilities
│   │
│   ├── control.py                # Direct API methods (balance, task management)
│   ├── recaptcha.py              # ReCaptcha V2/V3/Enterprise
│   ├── cloudflare.py             # Cloudflare Turnstile/Challenge
│   ├── gee_test.py               # GeeTest V3/V4
│   ├── datadome_slider.py        # DataDome slider captcha
│   ├── mt_captcha.py             # MtCaptcha
│   ├── aws_waf.py                # AWS WAF bypass
│   ├── friendly_captcha.py       # FriendlyCaptcha
│   ├── yandex.py                 # Yandex SmartCaptcha
│   ├── image_to_text.py          # OCR text extraction
│   ├── vision_engine.py          # AI-based image recognition
│   ├── __init__.py               # Package entry (exports version)
│   └── __version__.py            # Version string
│
├── tests/                        # Pytest test suite (mirrors src/ structure)
│   ├── conftest.py               # Pytest fixtures and configuration
│   ├── test_control.py           # Control class tests
│   ├── test_core.py              # Core module tests
│   ├── test_recaptcha.py         # ReCaptcha tests
│   ├── test_cloudflare.py        # Cloudflare tests
│   ├── test_instrument.py        # Instrument tests
│   └── ...                       # One test file per service
│
├── docs/                         # Sphinx documentation
│   ├── source/                   # Documentation source files
│   └── AGENTS.md                 # Documentation module context
│
├── .github/workflows/            # CI/CD pipelines
│   ├── build.yml                 # Package build
│   ├── test.yml                  # Test execution
│   ├── lint.yml                  # Code quality checks
│   ├── sphinx.yml                # Documentation build
│   └── install.yml               # Installation verification
│
├── pyproject.toml                # Build, dependency, tool configuration
├── Makefile                      # Developer convenience commands
├── README.md                     # Usage guide and quick start
├── AGENTS.md                     # Project knowledge base (for LLMs)
└── uv.lock                       # Dependency lock file (uv package manager)
```

**Where to Look**:
- **Adding a new captcha type**: Create new file in `src/python3_capsolver/`, inherit from `CaptchaParams`, follow pattern in `recaptcha.py`
- **Changing API communication**: Modify instrument classes in `src/python3_capsolver/core/`
- **Updating serialization**: Edit `src/python3_capsolver/core/serializer.py`
- **Adding captcha types**: Update `CaptchaTypeEnm` in `src/python3_capsolver/core/enum.py`
- **Test patterns**: See `tests/test_recaptcha.py` for service tests, `tests/test_core.py` for core tests

## 4. Life of a Request / Primary Data Flow

### Synchronous Flow (e.g., ReCaptcha solving)

1. **Initialization** (`recaptcha.py:ReCaptcha.__init__()`):
   - User instantiates `ReCaptcha(api_key="...", captcha_type=CaptchaTypeEnm.ReCaptchaV2Task)`
   - Calls `CaptchaParams.__init__()` which:
     - Serializes API key into `create_task_payload` (via `RequestCreateTaskSer`)
     - Initializes `task_params` with captcha type (via `TaskSer`)
     - Creates `get_result_params` (via `RequestGetTaskResultSer`)

2. **Handler Invocation** (`recaptcha.py:ReCaptcha.captcha_handler()` via inheritance):
   - User calls `.captcha_handler(task_payload={"websiteURL": "...", "websiteKey": "..."})` 
   - Updates `self.task_params` with user-provided payload
   - Instantiates `SIOCaptchaInstrument(captcha_params=self)`

3. **Task Creation** (`sio_captcha_instrument.py:SIOCaptchaInstrument.processing_captcha()`):
   - Sends POST to `{request_url}/createTask` with serialized payload
   - Receives `taskId` in response

4. **Result Polling** (`sio_captcha_instrument.py`):
   - Polls `{request_url}/getTaskResult` with `taskId` at intervals (`sleep_time`, default 5s)
   - Retries on transient failures (via `requests.Retry` adapter, 5 attempts)
   - Continues until status is `ready`, `failed`, or retry limit exceeded

5. **Response**:
   - Returns dict with `errorId`, `taskId`, `status`, `solution` fields
   - User extracts `solution` object containing captcha solution

### Asynchronous Flow

Identical to sync flow, except:
- Uses `AIOCaptchaInstrument` with `aiohttp.ClientSession`
- Retries via `tenacity` (async retries decorator)
- Handler is `await solver.aio_captcha_handler(task_payload)`

### Context Manager Flow

Both sync and async classes support context managers for automatic session cleanup:

```python
# Sync
with ReCaptcha(api_key="...") as solver:
    result = solver.captcha_handler(task_payload)

# Async
async with ReCaptcha(api_key="...") as solver:
    result = await solver.aio_captcha_handler(task_payload)
```

**Evidence Anchors**:
- `src/python3_capsolver/core/base.py`: Lines 25-41 (initialization), 43-61 (sync handler), 63-80 (async handler)
- `src/python3_capsolver/core/sio_captcha_instrument.py`: `processing_captcha()` method
- `src/python3_capsolver/core/aio_captcha_instrument.py`: Async `processing_captcha()` method
- `src/python3_capsolver/core/context_instr.py`: `SIOContextManager`, `AIOContextManager` mixins

## 5. Architectural Invariants & Constraints

### Invariant 1: Dual Sync/Async Support

- **Rule**: Every captcha-solving operation must provide both synchronous and asynchronous implementations.
- **Rationale**: Users may operate in sync or async codebases; the library must support both without forcing a choice.
- **Enforcement / Signals**: 
  - `CaptchaParams` base class defines both `captcha_handler()` and `aio_captcha_handler()` methods
  - Separate instrument classes (`SIOCaptchaInstrument`, `AIOCaptchaInstrument`) implement each mode
  - Tests include both sync and async variants (e.g., `test_recaptcha.py`)

### Invariant 2: Service Classes Are Thin Wrappers

- **Rule**: Service-specific classes (e.g., `ReCaptcha`, `Cloudflare`) must not contain HTTP logic or API communication code. They only specify captcha type and inherit behavior from `CaptchaParams`.
- **Rationale**: Separation of concerns—API communication is infrastructure, captcha parameters are domain logic. This enables easy addition of new captcha types.
- **Enforcement / Signals**:
  - All service classes inherit from `CaptchaParams` and typically only define `__init__()` (see `recaptcha.py:79-81`, 3 lines total)
  - Code review / lint checks would flag HTTP calls in service files

### Invariant 3: Serialization via msgspec

- **Rule**: All request/response serialization must use `msgspec.Struct` classes, not raw dicts or `json` module.
- **Rationale**: Performance—`msgspec` is significantly faster than `json` for serialization/deserialization.
- **Enforcement / Signals**:
  - `src/python3_capsolver/core/serializer.py` defines `RequestCreateTaskSer`, `CaptchaResponseSer`, etc.
  - Dependencies list `msgspec` but not alternative serializers
  - `pyproject.toml` explicitly notes "msgspec preferred over json for performance" (AGENTS.md)

### Invariant 4: Retry Logic Is Mandatory

- **Rule**: All HTTP requests must include retry logic with exponential backoff.
- **Rationale**: Captcha-solving is time-sensitive and external API calls may fail transiently; automatic retries improve reliability.
- **Enforcement / Signals**:
  - `SIOCaptchaInstrument` uses `requests.adapters.HTTPAdapter(max_retries=RETRIES)` (see `const.py` for retry config)
  - `AIOCaptchaInstrument` uses `tenacity` async retries (`ASYNC_RETRIES` in `const.py`)
  - Instruments are the only classes performing HTTP operations; base layer enforces their use

### Invariant 5: Type Safety via Enums

- **Rule**: Captcha types, endpoint names, and response statuses must use enumerations (`CaptchaTypeEnm`, `EndpointPostfixEnm`, `ResponseStatusEnm`), not raw strings.
- **Rationale**: Prevents typos, enables IDE autocomplete, documents valid values explicitly.
- **Enforcement / Signals**:
  - `CaptchaParams.__init__()` accepts `captcha_type: CaptchaTypeEnm` (typed parameter)
  - All service examples in docstrings use enum values (e.g., `CaptchaTypeEnm.ReCaptchaV2Task`)
  - `enum.py` defines all valid values in one location

### Invariant 6: No Direct HTTP Calls in Service Layer

- **Rule**: Service classes (`recaptcha.py`, `cloudflare.py`, etc.) must not import or use `requests`/`aiohttp` directly. All HTTP operations go through instruments.
- **Rationale**: Maintains separation of concerns, enables consistent retry/error-handling logic.
- **Enforcement / Signals**:
  - Service classes import only from `.core.base` and `.core.enum`
  - Instruments encapsulate all HTTP session management
  - Static analysis / linting would catch violations

### Invariant 7: Context Manager Support

- **Rule**: All captcha-solving classes must support Python context managers (`with` / `async with`) for automatic resource cleanup.
- **Rationale**: Ensures HTTP sessions are properly closed, prevents resource leaks.
- **Enforcement / Signals**:
  - `CaptchaParams` inherits from `SIOContextManager` and `AIOContextManager` (see `base.py:14`)
  - Context managers defined in `src/python3_capsolver/core/context_instr.py`
  - Usage examples in docstrings show context manager patterns

## 6. Documentation Strategy

### Documentation Hierarchy

**ARCHITECTURE.md** (this document):
- High-level system map and component relationships
- Architectural invariants and constraints
- Primary data flow and execution paths
- Physical code map ("where is X?")
- Stable information unlikely to change frequently

**Module-Level AGENTS.md/README.md** files:
- `AGENTS.md` (root): Project overview, structure, conventions, commands
- `src/python3_capsolver/AGENTS.md`: Package-level context, service list, usage patterns
- `src/python3_capsolver/core/AGENTS.md`: Core module details, class responsibilities, conventions
- Module docstrings: Class/function-level documentation with examples

**External Documentation**:
- Sphinx documentation in `docs/` directory (generated from docstrings)
- README.md: Quick start, installation, usage examples
- CHANGELOG.md: Version history and breaking changes

### What Belongs Where

| Information Type | Location |
|------------------|----------|
| System architecture, boundaries | ARCHITECTURE.md |
| Dependency rules, invariants | ARCHITECTURE.md |
| "Where is X?" questions | ARCHITECTURE.md (Code Map) |
| Module purpose, structure | `<module>/AGENTS.md` |
| Class/function usage examples | Docstrings (inline) |
| Installation, quick start | README.md |
| API parameter details | Sphinx docs (auto-generated) |
| Version changes | CHANGELOG.md |
| Development workflows | AGENTS.md (COMMANDS section) |

### Documentation Conventions

- **AGENTS.md files**: Generated knowledge base for LLMs and developers, following consistent template (OVERVIEW, STRUCTURE, WHERE TO LOOK, CONVENTIONS, COMMANDS)
- **Docstrings**: Google-style with Args, Returns, Examples, Notes sections
- **Type hints**: Full type annotations on all public APIs
- **Code examples**: Both sync and async variants shown in docstrings

### Evidence Anchors for Documentation

- Root `AGENTS.md`: Lines 1-41 (project structure, conventions, commands)
- `src/python3_capsolver/AGENTS.md`: Service pattern, dual handlers, retry logic
- `src/python3_capsolver/core/AGENTS.md`: Instrument patterns, serialization, retries
- `pyproject.toml`: Tool configuration (black, isort, pytest)
- `docs/`: Sphinx documentation source (auto-generated from docstrings)
