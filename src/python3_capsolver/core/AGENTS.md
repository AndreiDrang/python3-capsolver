# AGENTS.md

## Scope

Core infrastructure shared by all captcha services: base classes, HTTP instruments, serialization, enums, and constants.

## What lives here

```text
core/
├── base.py                    # CaptchaParams: merges payloads, delegates to instruments
├── captcha_instrument.py      # CaptchaInstrumentBase + FileInstrument (~221 lines)
├── sio_captcha_instrument.py  # SIOCaptchaInstrument: sync HTTP via requests
├── aio_captcha_instrument.py  # AIOCaptchaInstrument: async HTTP via aiohttp + tenacity
├── serializer.py              # msgspec.Struct classes for API payloads/responses
├── enum.py                    # CaptchaTypeEnm, ResponseStatusEnm, EndpointPostfixEnm
├── const.py                   # REQUEST_URL, RETRIES, sleep intervals, status codes
├── context_instr.py           # SIOContextManager, AIOContextManager mixins
├── utils.py                   # attempts_generator and helpers
└── __init__.py                # Empty — import via full path
```

## Local boundaries and invariants

- `captcha_instrument.py` contains both `CaptchaInstrumentBase` (abstract) and `FileInstrument` (file/URL/base64 processing) — edits here affect every service
- Instruments are the only place `requests` and `aiohttp` are imported — service layer must never touch HTTP libraries
- All serialization uses `msgspec.Struct` with `to_dict()` — never use the `json` module directly
- Enums in `enum.py` are the single source of truth for captcha types, response statuses, and endpoint names
- `base.py:CaptchaParams` is the single entry point; service classes inherit it and add only type-specific `__init__` params

## Safe change rules

- Adding a new captcha type requires updating `CaptchaTypeEnm` in `enum.py` and optionally adding structs to `serializer.py`
- Changes to `captcha_instrument.py` are high-impact: it is shared by all services and both sync/async paths
- Retry configuration lives in `const.py` (`RETRIES`, `ASYNC_RETRIES`) — do not hardcode retry counts in instruments
- `context_instr.py` provides `__enter__`/`__exit__` and `__aenter__`/`__aexit__` — all services depend on these mixins
- `__init__.py` is intentionally empty; do not add re-exports
