import pytest

from src.tests.conftest import BaseTest
from python3_captchaai.core.enum import ProxyType, ResponseStatusEnm
from python3_captchaai.mt_captcha import MtCaptcha
from python3_captchaai.core.serializer import CaptchaResponseSer

websiteURL = "https://www.mtcaptcha.com/#mtcaptcha-dem"
websiteKey = "MTPublic-tqNCRE0GS"
proxy = "198.22.3.1:10001:user:pwd"


class TestMtCaptchaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in MtCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in MtCaptcha.__dict__.keys()


class TestMtCaptcha(BaseTest):
    proxyAddress = "0.0.0.0"
    proxyPort = 9999
    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_params(self, proxy_type: str):
        MtCaptcha(api_key=self.API_KEY, websiteURL=websiteURL, websiteKey=websiteKey, proxy=proxy)

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_params_context(self, proxy_type: str):
        with MtCaptcha(api_key=self.API_KEY, websiteURL=websiteURL, websiteKey=websiteKey, proxy=proxy) as instance:
            pass

    """
    Failed tests
    """

    def test_proxy_err(self):
        resp = MtCaptcha(
            api_key=self.API_KEY, websiteURL=websiteURL, websiteKey=websiteKey, proxy=proxy
        ).captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId is True
        assert resp.errorCode == "ERROR_INVALID_TASK_DATA"
        assert resp.solution is None

    async def test_aio_proxy_err(self):
        resp = await MtCaptcha(
            api_key=self.API_KEY, websiteURL=websiteURL, websiteKey=websiteKey, proxy=proxy
        ).aio_captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId is True
        assert resp.errorCode == "ERROR_INVALID_TASK_DATA"
        assert resp.solution is None
