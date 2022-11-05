import pytest

from src.tests.conftest import BaseTest
from python3_captchaai.recaptcha import ReCaptcha
from python3_captchaai.core.enums import CaptchaTypeEnm, ResponseStatusEnm
from python3_captchaai.core.serializer import CaptchaResponseSer

GOOGLE_KEY = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
PAGE_URL = "https://www.google.com/recaptcha/api2/demo"


class TestReCaptchaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in ReCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in ReCaptcha.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.Control,
                websiteURL=self.get_random_string(5),
                websiteKey=self.get_random_string(5),
            )


class TestReCaptchaV2ProxyLess(BaseTest):
    googlekey = GOOGLE_KEY
    pageurl = PAGE_URL

    captcha_type = CaptchaTypeEnm.ReCaptchaV2TaskProxyLess
    """
    Success tests
    """

    def test_solve(self):
        resp = ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
        ).captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Ready
        assert resp.errorId is False
        assert resp.ErrorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None

    def test_solve_context(self):
        with ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
        ) as instance:
            resp = instance.captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Ready
        assert resp.errorId is False
        assert resp.ErrorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None

    async def test_aio_solve(self):
        resp = await ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
        ).aio_captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Ready
        assert resp.errorId is False
        assert resp.ErrorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None

    async def test_aio_solve_context(self):
        with ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
        ) as instance:
            resp = await instance.aio_captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Ready
        assert resp.errorId is False
        assert resp.ErrorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None

    """
    Failed tests
    """

    def test_api_key_err(self):
        with pytest.raises(Exception):
            ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
            )
