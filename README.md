# python3-capsolver

[![Capsolver.png](https://s.vyjava.xyz/files/2024/12-December/17/109278aa/Capsolver.png)](https://vyjava.xyz/dashboard/image/109278aa-961a-4503-bed0-0a9c838dcef2)

<hr>

[![PyPI version](https://badge.fury.io/py/python3-capsolver.svg)](https://badge.fury.io/py/python3-capsolver)
[![Python versions](https://img.shields.io/pypi/pyversions/python3-capsolver.svg?logo=python&logoColor=FBE072)](https://badge.fury.io/py/python3-capsolver)
[![Downloads](https://static.pepy.tech/badge/python3-capsolver/month)](https://pepy.tech/project/python3-capsolver)
[![Static Badge](https://img.shields.io/badge/docs-Sphinx-green?label=Documentation&labelColor=gray)](https://andreidrang.github.io/python3-capsolver/)

[![Maintainability](https://api.codeclimate.com/v1/badges/3c30167b5fb37a0775ea/maintainability)](https://codeclimate.com/github/AndreiDrang/python3-capsolver/maintainability)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/323d4eda0fe1477bbea8fe8902b9e97e)](https://www.codacy.com/gh/AndreiDrang/python3-capsolver/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AndreiDrang/python3-capsolver&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/AndreiDrang/python3-capsolver/branch/main/graph/badge.svg?token=2L4VVIF4G8)](https://codecov.io/gh/AndreiDrang/python3-capsolver)

[![Sphinx build](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/sphinx.yml/badge.svg?branch=release)](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/sphinx.yml)
[![Build](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/build.yml)
[![Installation](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/install.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/install.yml)
[![Tests](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/test.yml)
[![Lint](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-capsolver/actions/workflows/lint.yml)


Python 3 library for [Capsolver](https://dashboard.capsolver.com/passport/register?inviteCode=kQTn-tG07Jb1) service API.
Tested on UNIX based OS.

The library is intended for software developers and is used to work with the [Capsolver](https://dashboard.capsolver.com/passport/register?inviteCode=kQTn-tG07Jb1) service API.

## Features
- **Modern Tooling**: Uses `uv` for fast, reliable dependency management and environment isolation.
- **Sync & Async Support**: Full support for both synchronous (`requests`) and asynchronous (`aiohttp`) operations.
- **Type Safety**: Enums for captcha types and response statuses.
- **Resilience**: Built-in retries using `tenacity`.
- **Performance**: High-speed JSON serialization with `msgspec`.
- **Coverage**: Supports ReCaptcha (V2/V3), Cloudflare, DataDome, GeeTest, MtCaptcha, AWS WAF, Yandex, and ImageToText.

## How to install?

We recommend using the latest version of Python. `python3-capsolver` supports Python 3.8+.

### Development (using uv)

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable dependency management.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync --all-groups
```

### Production (pip)

```bash
pip install python3-capsolver
```

## How to use?

Detailed documentation is available on the [website](https://andreidrang.github.io/python3-capsolver/).

### Quick Start

#### Synchronous Example (ImageToText)
```python
from python3_capsolver.image_to_text import ImageToText

# 1. Initialize with API Key
solver = ImageToText(api_key="YOUR_API_KEY")

# 2. Solve
result = solver.captcha_handler(
    task_payload={
        "body": "base64_encoded_image_string"
    }
)

# 3. Check result
if result["errorId"] == 0:
    print("Solution:", result["solution"])
else:
    print("Error:", result["errorCode"])
```

#### Asynchronous Example (ReCaptcha)
```python
import asyncio
from python3_capsolver.recaptcha import ReCaptcha
from python3_capsolver.core.enum import CaptchaTypeEnm

async def main():
    # 1. Initialize
    solver = ReCaptcha(
        api_key="YOUR_API_KEY", 
        captcha_type=CaptchaTypeEnm.ReCaptchaV2TaskProxyLess
    )

    # 2. Solve
    result = await solver.aio_captcha_handler(
        task_payload={
            "websiteURL": "https://example.com",
            "websiteKey": "SITE_KEY"
        }
    )
    
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Supported Captcha Types
- **ReCaptcha**: V2 (Task/Enterprise), V3 (Task/Enterprise)
- **HCaptcha**: Task, Enterprise
- **Cloudflare**: Turnstile
- **GeeTest**: V3, V4
- **DataDome**: Slider
- **MtCaptcha**
- **AWS WAF**
- **Yandex SmartCaptcha**
- **ImageToText**: General image CAPTCHAs

## Documentation & Context (For LLMs)
- **Project Structure**: See `AGENTS.md` in root and subdirectories for internal architecture.
- **Entry Points**: `src/python3_capsolver/*.py` contains service-specific classes (e.g., `ReCaptcha`, `HCaptcha`).
- **Core Logic**: `src/python3_capsolver/core/base.py` handles the API communication loop.
- **Enums**: Use `python3_capsolver.core.enum` for type-safe parameters.

## How to test?

The project uses `uv` for testing and development tasks.

```bash
# 1. Set API_KEY in your environment (get this value from your account)
export API_KEY="your_api_key_here"

# 2. Run tests (uses uv internally)
make tests

# Other useful make targets:
# make install     # Install dependencies with uv sync
# make lint        # Run linting checks
# make build       # Build the package
# make doc         # Generate documentation
```

All `make` commands automatically use `uv` to run commands in the isolated environment.


### Changelog

See [CHANGELOG.md](https://github.com/AndreiDrang/python3-capsolver/blob/main/CHANGELOG.md) for version history and detailed changes.

### How to get API Key to work with the library
1. On the page - https://dashboard.capsolver.com/overview/user-center
2. Find it: [![img.png](https://s.vyjava.xyz/files/2024/12-December/17/ae8d4fbf/img.png)](https://vyjava.xyz/dashboard/image/ae8d4fbf-7451-441d-8984-79b1a7adbe27)

### Contacts

If you have any questions, please send a message to the [Telegram](https://t.me/pythoncaptcha) chat room.

Or email python-captcha@pm.me
