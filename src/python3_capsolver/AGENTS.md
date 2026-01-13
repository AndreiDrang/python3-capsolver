# PYTHON3_CAPSOLVER PACKAGE

**Generated:** 2026-01-13

## OVERVIEW
Main library package containing service-specific captcha solving implementations. Provides high-level interfaces for various captcha types (ReCaptcha, Cloudflare Turnstile, DataDome, etc.) through a unified API.

Each service class inherits from `core.CaptchaParams` and implements synchronous (`requests`) and asynchronous (`aiohttp`) solving methods with automatic retry logic and response polling.

## STRUCTURE
```
src/python3_capsolver/
├── core/                     # Base classes, instruments, serializers
├── control.py                # Control class for direct API methods
├── recaptcha.py              # ReCaptcha V2/V3/Enterprise implementations
├── cloudflare.py             # Cloudflare Turnstile/Challenge solver
├── vision_engine.py          # AI-based image recognition
├── image_to_text.py          # OCR text extraction
├── datadome_slider.py        # DataDome slider captcha
├── mt_captcha.py             # MtCaptcha solver
├── gee_test.py               # GeeTest solver
├── aws_waf.py                # AWS WAF bypass
├── friendly_captcha.py       # FriendlyCaptcha solver
└── yandex.py                 # Yandex captcha solver
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
