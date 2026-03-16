# TESTS SUITE

**Generated:** 2026-03-15
**Commit:** b797332

## OVERVIEW
Pytest-based test suite validating API integration, dual-mode (sync/async) operations, and error handling for all captcha services.

## STRUCTURE
```
tests/
├── conftest.py              # BaseTest class, fixtures, test utilities
├── test_*.py                # Test modules (match source structure)
└── files/                   # Test assets (captcha_example.jpeg)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Base Test Class** | `tests/conftest.py` | `BaseTest` with utilities (`get_random_string`, `read_image`) |
| **Fixtures** | `tests/conftest.py` | `delay_func` (1s), `delay_class` (2s) for rate limiting |
| **Core Tests** | `tests/test_core.py` | Base logic, retries, enums, context managers |
| **Service Tests** | `tests/test_*.py` | Per-service tests (recaptcha, cloudflare, datadome, etc.) |
| **Instrument Tests** | `tests/test_instrument.py` | File processing, instruments |
| **Pytest Config** | `pyproject.toml` | `asyncio_mode = "auto"`, testpaths |

## CONVENTIONS
- **Framework**: Pytest 7.0+ with `pytest-asyncio` (auto mode).
- **Dual Testing**: Every sync test (`def test_*`) has async counterpart (`async def test_aio_*`).
- **Parametrization**: Use `@pytest.mark.parametrize` for multiple captcha types in single test.
- **Base Class**: All tests inherit from `BaseTest` for common utilities and rate limiting.
- **Context Managers**: Test both `with` and `async with` patterns for resource cleanup.
- **Rate Limiting**: Default delays (1s function, 2s class) to avoid API throttling.
- **Error Testing**: Verify `errorId`, `errorCode`, and `solution=None` for invalid keys.

## COMMANDS
```bash
# Run all tests
uv run pytest tests/

# Run with coverage
make tests    # Runs coverage + HTML + XML reports

# Coverage reports
coverage/html/     # HTML report
coverage/coverage.xml  # XML for CI
```

## NOTES
- **API Key**: Requires `API_KEY` environment variable
- **Test Files**: 15 test modules, ~1.5k lines total
- **Rate Limiting**: Built-in delays prevent API throttling during test runs
