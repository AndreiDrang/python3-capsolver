# PROJECT KNOWLEDGE BASE

**Generated:** 2026-03-15
**Commit:** b797332
**Branch:** main

## OVERVIEW
Python 3.8+ library for Capsolver service API. Dual sync (`requests`) / async (`aiohttp`) support. `msgspec` for serialization, `tenacity` for retries.

## STRUCTURE
```
./
├── src/python3_capsolver/    # Main library (service implementations)
│   ├── core/                 # Base classes, instruments, serializers
│   └── *.py                  # Service-specific (ReCaptcha, Cloudflare, etc.)
├── tests/                    # Pytest suite (matches source structure)
├── docs/                     # Sphinx documentation
├── ARCHITECTURE.md           # System architecture (matklad-style)
└── pyproject.toml            # Build, uv, pytest, black/isort config
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Architecture** | `ARCHITECTURE.md` | Layered design, invariants, life of a request |
| **Base Logic** | `src/python3_capsolver/core/` | `base.py`, `serializer.py`, `enum.py`, instruments |
| **Service Implementations** | `src/python3_capsolver/*.py` | `recaptcha.py`, `cloudflare.py`, `control.py` |
| **Tests** | `tests/` | `conftest.py` (BaseTest, fixtures), per-service tests |
| **Configuration** | `pyproject.toml` | uv, black (120), isort, pytest (asyncio auto) |
| **Commands** | `Makefile` | `make tests`, `make build`, `make upload` |

## CONVENTIONS
- **Toolchain**: `uv` for package management (`uv sync`, `uv run`, `uv build`, `uv publish`)
- **Formatter**: `black` (line-length 120), `isort` (profile "black")
- **Cleanup**: `autoflake` (remove unused imports/variables)
- **Serialization**: `msgspec` (not `json`) for performance
- **Concurrency**: Dual sync/async required for all instruments
- **Retries**: `tenacity` (async), `requests.Retry` (sync) — 5 attempts, exponential backoff
- **Testing**: pytest 7.0+, `pytest-asyncio` (auto mode), rate-limiting fixtures (1s func, 2s class)

## ANTI-PATTERNS (THIS PROJECT)
- **Empty `__init__.py` files**: `src/python3_capsolver/__init__.py` only exports `__version__`; `core/__init__.py` is completely empty. Users must import via full paths (`from python3_capsolver.recaptcha import ReCaptcha`)
- **AGENTS.md in package dirs**: Will ship with distribution unless excluded in `pyproject.toml`
- **No CLI entry points**: Library-only, no console_scripts defined

## UNIQUE STYLES
- **Service Pattern**: Each captcha service inherits from `CaptchaParams` with `captcha_handler()` (sync) + `aio_captcha_handler()` (async)
- **Task Payload**: Dict merged with internal params, passed to `create_task()` API
- **Context Managers**: All services support `with` / `async with` for session cleanup
- **Test Duplication**: Every sync test (`def test_*`) has async counterpart (`async def test_aio_*`)

## COMMANDS
```bash
# Development
uv sync --all-groups           # Install all dependencies
uv run pytest tests/           # Run tests
uv run black src/ tests/       # Format
uv run isort src/ tests/       # Sort imports

# Build & Publish
uv build                       # Build wheel/sdist
uv publish                     # Upload to PyPI

# Documentation
cd docs/ && uv run --group docs make html -e
```

## NOTES
- **API Key**: Tests require `API_KEY` environment variable
- **Coverage**: HTML reports in `coverage/html/`, XML in `coverage/coverage.xml`
- **Python Support**: 3.8–3.12 (tested via `target-version = ['py310']`)
- **Dependencies**: `requests>=2.21.0`, `aiohttp>=3.9.2`, `msgspec>=0.18,<=0.21`, `tenacity>=8,<10`
