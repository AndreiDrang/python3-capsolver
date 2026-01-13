# CORE MODULE

**Generated:** 2026-01-13

## OVERVIEW
Core module provides foundational classes for synchronous (`requests`) and asynchronous (`aiohttp`) captcha solving operations.

Base classes establish patterns for Sync/Async instruments, enabling dual concurrency support across the library. Serialization leverages `msgspec` for high-performance JSON handling.

## STRUCTURE
```
src/python3_capsolver/core/
├── base.py                    # CaptchaParams entry class (Sync/Async handlers)
├── captcha_instrument.py      # CaptchaInstrumentBase, FileInstrument
├── aio_captcha_instrument.py  # AIOCaptchaInstrument (async implementation)
├── sio_captcha_instrument.py  # SIOCaptchaInstrument (sync implementation)
├── serializer.py              # Request/Response msgspec Struct classes
├── enum.py                    # EndpointPostfixEnm, CaptchaTypeEnm, ResponseStatusEnm
├── const.py                   # API URLs, retry configurations
└── utils.py                   # Utility functions (attempts_generator)
```

## WHERE TO LOOK
| Task | File | Notes |
|------|------|-------|
| **Entry Point** | `base.py` | `CaptchaParams` class with `captcha_handler()` and `aio_captcha_handler()` |
| **Base Classes** | `captcha_instrument.py` | `CaptchaInstrumentBase` for instruments, `FileInstrument` for file processing |
| **Sync Instrument** | `sio_captcha_instrument.py` | `SIOCaptchaInstrument` - requests-based implementation |
| **Async Instrument** | `aio_captcha_instrument.py` | `AIOCaptchaInstrument` - aiohttp-based implementation |
| **Serialization** | `serializer.py` | `PostRequestSer`, `CaptchaResponseSer`, `MyBaseModel.to_dict()` |
| **Enums** | `enum.py` | `CaptchaTypeEnm`, `ResponseStatusEnm`, `EndpointPostfixEnm` |
| **Configuration** | `const.py` | `REQUEST_URL`, `RETRIES`, `VALID_STATUS_CODES` |

## CONVENTIONS
- **Base Classes**: All instruments inherit from `CaptchaInstrumentBase`
- **Dual Support**: Every captcha operation provides both sync and async methods
- **Serialization**: `msgspec.Struct` classes with `to_dict()` method for API payloads
- **Retries**: `tenacity` for async, `requests.Retry` for sync (5 attempts, exponential backoff)
- **File Processing**: `FileInstrument` handles local files, URLs, and base64 in both sync/async contexts
- **Session Management**: Instruments maintain their own HTTP sessions with retry adapters
