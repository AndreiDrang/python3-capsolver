import pytest

from src.tests.conftest import BaseTest
from python3_capsolver.core.enum import ProxyType, ResponseStatusEnm
from python3_capsolver.mt_captcha import MtCaptcha
from python3_capsolver.core.serializer import CaptchaResponseSer

websiteURL = "https://www.mtcaptcha.com/#mtcaptcha-dem"
websiteKey = "MTPublic-tqNCRE0GS"
proxy = "198.22.3.1:10001:user:pwd"


class TestMtCaptchaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in MtCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in MtCaptcha.__dict__.keys()

    def test_no_website_url(self):
        with pytest.raises(TypeError):
            MtCaptcha(api_key=self.API_KEY, websiteKey=websiteKey, proxy=proxy)

    def test_no_website_key(self):
        with pytest.raises(TypeError):
            MtCaptcha(api_key=self.API_KEY, websiteURL=websiteURL, proxy=proxy)

    def test_no_proxy(self):
        with pytest.raises(TypeError):
            MtCaptcha(api_key=self.API_KEY, websiteURL=websiteURL, websiteKey=websiteKey)


class TestMtCaptcha(BaseTest):
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
