import pytest

from src.tests.conftest import BaseTest
from python3_captchaai.core.enum import CaptchaTypeEnm
from python3_captchaai.fun_captcha import FunCaptcha

websiteURL = "https://api.funcaptcha.com/fc/api/nojs/"
websitePublicKey = "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC"
funcaptchaApiJSSubdomain = "https://api.funcaptcha.com/"

captcha_types = (
    CaptchaTypeEnm.FuncaptchaTask,
    CaptchaTypeEnm.FuncaptchaTaskProxyless,
    CaptchaTypeEnm.FunCaptchaClassification,
)


class TestFunCaptchaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in FunCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in FunCaptcha.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            FunCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.Control,
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            )

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            FunCaptcha(
                api_key=self.get_random_string(36),
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            )
