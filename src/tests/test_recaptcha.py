import pytest

from src.tests.conftest import BaseTest
from python3_captchaai.recaptcha import ReCaptcha
from python3_captchaai.core.enums import CaptchaTypeEnm, ResponseStatusEnm
from python3_captchaai.core.serializer import CaptchaResponseSer


class TestReCaptcha(BaseTest):
    googlekey = "6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH"
    pageurl = "https://rucaptcha.com/demo/recaptcha-v2"
    """
    Success tests
    """

    def test_captcha_handler_exist(self):
        assert "captcha_handler" in ReCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in ReCaptcha.__dict__.keys()

    def test_solve_v2_task_proxy_less(self):
        resp = ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.ReCaptchaV2TaskProxyLess,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
        ).captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Ready
        assert resp.errorId is False
        assert resp.ErrorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None

    def test_solve_v2_task_proxy_less_context(self):
        with ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.ReCaptchaV2TaskProxyLess,
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

    async def test_aio_solve_v2_task_proxy_less(self):
        resp = await ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.ReCaptchaV2TaskProxyLess,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
        ).aio_captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Ready
        assert resp.errorId is False
        assert resp.ErrorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None

    async def test_aio_solve_v2_task_proxy_less_context(self):
        with ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=CaptchaTypeEnm.ReCaptchaV2TaskProxyLess,
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

    def test_captcha_handler_api_key_err(self):
        with pytest.raises(Exception):
            ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.ReCaptchaV2TaskProxyLess,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
            ).captcha_handler()

    async def test_aio_captcha_handler_api_key_err(self):
        with pytest.raises(Exception):
            await ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.ReCaptchaV2TaskProxyLess,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
            ).aio_captcha_handler()
