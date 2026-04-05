# AGENTS.md

## Scope

Service implementations for individual captcha types. Each file is a self-contained solver class.

## What lives here

```text
src/python3_capsolver/
├── core/                     # Base classes, instruments, serializers (own AGENTS.md)
├── control.py                # Raw API: get_balance, create_task, get_task_result
├── recaptcha.py              # ReCaptcha V2/V3/Enterprise
├── cloudflare.py             # Cloudflare Turnstile/Challenge
├── gee_test.py               # GeeTest V3/V4
├── datadome_slider.py        # DataDome slider
├── mt_captcha.py             # MtCaptcha
├── aws_waf.py                # AWS WAF bypass
├── friendly_captcha.py       # FriendlyCaptcha
├── yandex.py                 # Yandex SmartCaptcha
├── image_to_text.py          # OCR text extraction
├── vision_engine.py          # AI-based image recognition
├── __init__.py               # Exports only __version__
└── __version__.py            # Version string
```

## Local boundaries and invariants

- Service classes inherit `CaptchaParams` and define only `__init__` with captcha-type-specific params
- No HTTP imports (`requests`, `aiohttp`) allowed in service files — all HTTP goes through `core/` instruments
- Every service must provide both `captcha_handler()` (sync) and `aio_captcha_handler()` (async) via inheritance
- Every service must support context managers (`with` / `async with`) via `SIOContextManager` + `AIOContextManager` mixins

## Safe change rules

- To add a new captcha type: create `new_service.py`, inherit `CaptchaParams`, add type to `CaptchaTypeEnm` in `core/enum.py`, add serializer structs if needed in `core/serializer.py`
- `control.py` is unique: it provides raw API methods (`get_balance`, `create_task`, `get_task_result`) without the create-then-poll abstraction — do not convert it to the standard pattern
- Users import via full path (`from python3_capsolver.recaptcha import ReCaptcha`) — do not add re-exports to `__init__.py`
- This file ships inside the wheel; keep it concise and avoid sensitive information
