# PYTHON3_CAPSOLVER PACKAGE

**Generated:** 2026-03-15
**Commit:** b797332

## OVERVIEW
Main library package containing service-specific captcha solving implementations. Provides high-level interfaces for various captcha types (ReCaptcha, Cloudflare Turnstile, DataDome, etc.) through a unified API.

Each service class inherits from `core.CaptchaParams` and implements synchronous (`requests`) and asynchronous (`aiohttp`) solving methods with automatic retry logic and response polling.

## STRUCTURE
```
src/python3_capsolver/
├── core/                     # Base classes, instruments, serializers
├── control.py                # Direct API access (get_balance, create_task, get_task_result)
├── recaptcha.py              # ReCaptcha V2/V3/Enterprise
├── cloudflare.py             # Cloudflare Turnstile/Challenge
├── vision_engine.py          # AI-based image recognition
├── image_to_text.py          # OCR text extraction
├── datadome_slider.py        # DataDome slider captcha
├── mt_captcha.py             # MtCaptcha solver
├── gee_test.py               # GeeTest solver
├── aws_waf.py                # AWS WAF bypass
├── friendly_captcha.py       # FriendlyCaptcha solver
├── yandex.py                 # Yandex captcha solver
├── __init__.py               # Exports only __version__ (minimal)
└── __version__.py            # Version string
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Direct API Access** | `control.py` | `Control.get_balance()`, `create_task()`, `get_task_result()` |
| **ReCaptcha** | `recaptcha.py` | V2, V3, Enterprise variants |
| **Cloudflare** | `cloudflare.py` | Turnstile, Challenge modes |
| **Image-based** | `vision_engine.py`, `image_to_text.py` | AI recognition, OCR |
| **Other Services** | `*.py` | DataDome, GeeTest, AWS WAF, etc. |
| **Base Logic** | `core/` | `CaptchaParams`, instruments, serializers |

## CONVENTIONS
- **Service Pattern**: Each service class inherits from `CaptchaParams` with `api_key` and `captcha_type` params
- **Dual Handlers**: All services provide `captcha_handler()` (sync) and `aio_captcha_handler()` (async)
- **Retry Logic**: Built-in exponential backoff with configurable `sleep_time` (default: 5s)
- **Task Payload**: Passed via `task_payload` dict, merged with internal task params
- **Response Structure**: Returns dict with `errorId`, `taskId`, `status`, `solution` fields
- **Context Managers**: Support `with` and `async with` for session cleanup

## ANTI-PATTERNS (THIS PACKAGE)
- **Minimal `__init__.py`**: Does NOT export service classes. Users cannot do `from python3_capsolver import ReCaptcha` — must use full path `from python3_capsolver.recaptcha import ReCaptcha`
- **AGENTS.md in package dir**: Will ship with distribution unless excluded in `pyproject.toml`

## UNIQUE STYLES
- **control.py (431 lines)**: Largest file, provides raw API access without abstraction
- **Service files**: 2-5k lines each, focused on single captcha type
- **No type stubs**: Type hints inline, no `.pyi` files
