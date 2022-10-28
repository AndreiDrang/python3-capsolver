import asyncio

from python_rucaptcha.enums import GeetestEnm
from python_rucaptcha.GeeTest import GeeTest, aioGeeTest


captcha_id = 'AHrlqAAAAAMAIzYK4V3-7c4AVc6jlA=='
# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f3182ca81755768608fa758570"
gt = GeeTest(
    rucaptcha_key=RUCAPTCHA_KEY,
    method=GeetestEnm.GEETEST_V4.value,
    pageurl="https://www.zocdoc.com/",
    captcha_id=captcha_id
)

print(gt.captcha_handler())
