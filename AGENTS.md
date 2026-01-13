# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-13

## OVERVIEW
Python 3.8+ library for Capsolver service API. Supports both synchronous (`requests`) and asynchronous (`aiohttp`) operations. Uses `msgspec` for high-performance JSON serialization.

## STRUCTURE
```
./
├── src/python3_capsolver/    # Main library package
│   ├── core/                 # Base classes, serializers, instruments
│   └── *.py                  # Service-specific implementations (ReCaptcha, Cloudflare, etc.)
├── tests/                    # Pytest suite
└── docs/                     # Sphinx documentation
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Base Logic** | `src/python3_capsolver/core/` | `base.py`, `serializer.py`, `enum.py` |
| **Service Implementations** | `src/python3_capsolver/*.py` | `recaptcha.py`, `cloudflare.py`, etc. |
| **Tests** | `tests/` | Matches source structure |
| **Configuration** | `pyproject.toml` | Build, dependency, tool config |

## CONVENTIONS
- **Formatter**: `black` (line-length 120), `isort` (profile "black").
- **Serialization**: `msgspec` preferred over `json` for performance.
- **Concurrency**: Dual support (Sync/Async) required for all instruments.
- **Retries**: `tenacity` library used for resilience.

## COMMANDS
```bash
make tests          # Run test suite
pip install .       # Install package locally
```

## NOTES
- Dependencies: `requests`, `aiohttp`, `msgspec`, `tenacity`.
- Requires `API_KEY` in environment for tests.

