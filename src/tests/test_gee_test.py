import pytest

from src.tests.conftest import BaseTest
from python3_captchaai.gee_test import GeeTest
from python3_captchaai.core.enum import CaptchaTypeEnm

PAGE_URL = "https://www.geetest.com/en/demo"
GT = "022397c99c9f646f6477822485f30404"
CHALLENGE = "a66f31a53a404af8d1f271eec5138aa1"
API_SUBDOMAIN = "api.geetest.com"


class TestGeeTestBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in GeeTest.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in GeeTest.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            GeeTest(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.Control,
                websiteURL="https://www.geetest.com/en/demo",
                gt="022397c99c9f646f6477822485f30404",
            )

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            GeeTest(
                api_key=self.get_random_string(36),
                websiteURL="https://www.geetest.com/en/demo",
                gt="022397c99c9f646f6477822485f30404",
            )
