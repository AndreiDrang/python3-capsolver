import pytest

from tests.conftest import BaseTest
from python3_capsolver.core.enum import MtCaptchaTypeEnm, ResponseStatusEnm
from python3_capsolver.mt_captcha import MtCaptcha
from python3_capsolver.core.serializer import CaptchaResponseSer

websiteURL = "https://www.mtcaptcha.com/#mtcaptcha-dem"
websiteKey = "MTPublic-tqNCRE0GS"
proxy = "198.22.3.1:10001:user:pwd"


class TestMtCaptchaBase(BaseTest):
    captcha_types = (MtCaptchaTypeEnm.MtCaptchaTask, MtCaptchaTypeEnm.MtCaptchaTaskProxyLess)

    def test_captcha_handler_exist(self):
        assert "captcha_handler" in MtCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in MtCaptcha.__dict__.keys()

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_no_website_url(self, captcha_type: str):
        with pytest.raises(TypeError):
            MtCaptcha(api_key=self.API_KEY, captcha_type=captcha_type, websiteKey=websiteKey, proxy=proxy)

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_no_website_key(self, captcha_type: str):
        with pytest.raises(TypeError):
            MtCaptcha(api_key=self.API_KEY, captcha_type=captcha_type, websiteURL=websiteURL, proxy=proxy)


class TestMtCaptcha(BaseTest):
    captcha_types = (MtCaptchaTypeEnm.MtCaptchaTask, MtCaptchaTypeEnm.MtCaptchaTaskProxyLess)
    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_params(self, proxy_type: str, captcha_type: str):
        MtCaptcha(
            api_key=self.API_KEY, captcha_type=captcha_type, websiteURL=websiteURL, websiteKey=websiteKey, proxy=proxy
        )

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_params_context(self, proxy_type: str, captcha_type: str):
        with MtCaptcha(
            api_key=self.API_KEY, captcha_type=captcha_type, websiteURL=websiteURL, websiteKey=websiteKey, proxy=proxy
        ) as instance:
            pass

    """
    Failed tests
    """

    def test_proxy_err(self):
        resp = MtCaptcha(
            api_key=self.API_KEY,
            captcha_type=MtCaptchaTypeEnm.MtCaptchaTask,
            websiteURL=websiteURL,
            websiteKey=websiteKey,
            proxy=proxy,
        ).captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId == 1
        assert resp.errorCode == "ERROR_PROXY_CONNECT_REFUSED"
        assert resp.solution is None

    async def test_aio_proxy_err(self):
        resp = await MtCaptcha(
            api_key=self.API_KEY,
            captcha_type=MtCaptchaTypeEnm.MtCaptchaTask,
            websiteURL=websiteURL,
            websiteKey=websiteKey,
            proxy=proxy,
        ).aio_captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId == 1
        assert resp.errorCode == "ERROR_PROXY_CONNECT_REFUSED"
        assert resp.solution is None
