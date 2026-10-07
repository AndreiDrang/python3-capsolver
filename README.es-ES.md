

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


Biblioteca de Python 3 para la API del servicio [Capsolver](https://dashboard.capsolver.com/passport/register?inviteCode=kQTn-tG07Jb1).
Probada en sistemas operativos basados en UNIX.

La biblioteca está destinada a desarrolladores de software y se utiliza para trabajar con la API del servicio [Capsolver](https://dashboard.capsolver.com/passport/register?inviteCode=kQTn-tG07Jb1).

## Características
- **Herramientas Modernas**: Utiliza `uv` para una gestión rápida y confiable de dependencias y aislamiento de entornos.
- **Soporte Síncrono y Asíncrono**: Soporte completo para operaciones tanto síncronas (`requests`) como asíncronas (`aiohttp`).
- **Seguridad de Tipos**: Enums para tipos de captcha y estados de respuesta.
- **Resiliencia**: Reintentos integrados utilizando `tenacity`.
- **Rendimiento**: Serialización JSON de alta velocidad con `msgspec`.
- **Cobertura**: Compatible con ReCaptcha (V2/V3), Cloudflare, DataDome, GeeTest, MtCaptcha, AWS WAF, Yandex e ImageToText.

## ¿Cómo instalarlo?

Recomendamos utilizar la versión más reciente de Python. `python3-capsolver` es compatible con Python 3.8+.

### Desarrollo (usando uv)

Este proyecto utiliza [uv](https://github.com/astral-sh/uv) para una gestión rápida y confiable de dependencias.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync --all-groups
```

### Producción (pip)

```bash
pip install python3-capsolver
```

## ¿Cómo usarlo?

La documentación detallada está disponible en el [sitio web](https://andreidrang.github.io/python3-capsolver/).

### Inicio Rápido

#### Ejemplo Síncrono (ImageToText)
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

#### Ejemplo Asíncrono (ReCaptcha)
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

## Tipos de Captcha Soportados
- **ReCaptcha**: V2 (Task/Enterprise), V3 (Task/Enterprise)
- **HCaptcha**: Task, Enterprise
- **Cloudflare**: Turnstile
- **GeeTest**: V3, V4
- **DataDome**: Slider
- **MtCaptcha**
- **AWS WAF**
- **Yandex SmartCaptcha**
- **ImageToText**: CAPTCHAS de imágenes generales

## Documentación y Contexto (Para LLMs)
- **Estructura del Proyecto**: Consulta `AGENTS.md` en la raíz y los subdirectorios para conocer la arquitectura interna.
- **Puntos de Entrada**: `src/python3_capsolver/*.py` contiene clases específicas de cada servicio (p. ej., `ReCaptcha`, `HCaptcha`).
- **Lógica Central**: `src/python3_capsolver/core/base.py` maneja el ciclo de comunicación con la API.
- **Enums**: Utiliza `python3_capsolver.core.enum` para parámetros con seguridad de tipos.

## ¿Cómo realizar pruebas?

El proyecto utiliza `uv` para tareas de pruebas y desarrollo.

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

Todos los comandos `make` utilizan automáticamente `uv` para ejecutar los comandos en el entorno aislado.


### Registro de Cambios

Consulta [CHANGELOG.md](https://github.com/AndreiDrang/python3-capsolver/blob/main/CHANGELOG.md) para el historial de versiones y cambios detallados.

### ¿Cómo obtener la clave API para usar la biblioteca?
1. En la página: https://dashboard.capsolver.com/overview/user-center
2. Búscala: [![img.png](https://s.vyjava.xyz/files/2024/12-December/17/ae8d4fbf/img.png)](https://vyjava.xyz/dashboard/image/ae8d4fbf-7451-441d-8984-79b1a7adbe27)

### Contacto

Si tienes alguna pregunta, envía un mensaje al chat de [Telegram](https://t.me/pythoncaptcha).

O envía un correo a python-captcha@pm.me
