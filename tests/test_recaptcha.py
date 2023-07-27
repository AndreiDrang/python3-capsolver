import pytest
from pydantic import ValidationError

from tests.conftest import BaseTest
from python3_capsolver.core.enum import ResponseStatusEnm, ReCaptchaV2TypeEnm, ReCaptchaV3TypeEnm
from python3_capsolver.recaptcha import ReCaptcha
from python3_capsolver.core.serializer import CaptchaResponseSer

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
                captcha_type="test",
                websiteURL=self.get_random_string(5),
                websiteKey=self.get_random_string(5),
            )

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            ReCaptcha(
                api_key=self.get_random_string(36),
                websiteURL=self.get_random_string(5),
                websiteKey=self.get_random_string(5),
            )


class TestReCaptchaV2ProxyLess(BaseTest):
    googlekey = GOOGLE_KEY
    pageurl = PAGE_URL

    captcha_types = (ReCaptchaV2TypeEnm.ReCaptchaV2TaskProxyLess, ReCaptchaV2TypeEnm.ReCaptchaV2EnterpriseTaskProxyLess)
    """
    Success tests
    """

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_params(self, captcha_type: str):
        ReCaptcha(api_key=self.API_KEY, captcha_type=captcha_type, websiteURL=self.pageurl, websiteKey=self.googlekey)

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_params_context(self, captcha_type: str):
        with ReCaptcha(
            api_key=self.API_KEY, captcha_type=captcha_type, websiteURL=self.pageurl, websiteKey=self.googlekey
        ) as instance:
            pass

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_solve(self, captcha_type: str):
        resp = ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
        ).captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Ready
        assert resp.errorId == 0
        assert resp.errorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None

    """def test_solve_context(self):
        with ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
        ) as instance:
            resp = instance.captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Ready
        assert resp.errorId == 0
        assert resp.errorCode is None
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
        assert resp.errorId == 0
        assert resp.errorCode is None
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
        assert resp.errorId == 0
        assert resp.errorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None"""

    """
    Failed tests
    """

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_no_website_key(self, captcha_type: str):
        with pytest.raises(TypeError):
            ReCaptcha(api_key=self.API_KEY, captcha_type=captcha_type, websiteURL=self.pageurl)

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_no_website_url(self, captcha_type: str):
        with pytest.raises(TypeError):
            ReCaptcha(api_key=self.API_KEY, captcha_type=captcha_type, websiteKey=self.googlekey)


class TestReCaptchaV2(BaseTest):
    googlekey = GOOGLE_KEY
    pageurl = PAGE_URL
    proxyAddress = "0.0.0.0"
    proxyPort = 9999
    captcha_types = (ReCaptchaV2TypeEnm.ReCaptchaV2Task, ReCaptchaV2TypeEnm.ReCaptchaV2EnterpriseTask)

    """
    Success tests
    """

    @pytest.mark.parametrize("captcha_type", captcha_types)
    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_params(self, proxy_type: str, captcha_type: str):
        ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        )

    @pytest.mark.parametrize("captcha_type", captcha_types)
    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_params_context(self, proxy_type: str, captcha_type: str):
        with ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        ) as instance:
            pass

    """
    Failed tests
    """

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_no_website_key(self, captcha_type: str):
        with pytest.raises(TypeError):
            ReCaptcha(api_key=self.API_KEY, captcha_type=captcha_type, websiteURL=self.pageurl)

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_no_website_url(self, captcha_type: str):
        with pytest.raises(TypeError):
            ReCaptcha(api_key=self.API_KEY, captcha_type=captcha_type, websiteKey=self.googlekey)


class TestReCaptchaV3ProxyLess(BaseTest):
    googlekey = GOOGLE_KEY
    pageurl = PAGE_URL

    pageAction = BaseTest().get_random_string(5)
    captcha_type = ReCaptchaV3TypeEnm.ReCaptchaV3TaskProxyLess

    """
    Success tests
    """

    def test_params(self):
        ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            pageAction=self.pageAction,
        )

    def test_params_context(self):
        with ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            pageAction=self.pageAction,
        ) as instance:
            pass

    """
    Failed tests
    """

    def test_no_website_key(self):
        with pytest.raises(TypeError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                pageAction=self.pageAction,
            )

    def test_no_website_url(self):
        with pytest.raises(TypeError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteKey=self.googlekey,
                pageAction=self.pageAction,
            )

    def test_no_page_action(self):
        with pytest.raises(ValidationError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
            )


class TestReCaptchaV3(BaseTest):
    googlekey = GOOGLE_KEY
    pageurl = PAGE_URL

    proxyAddress = "0.0.0.0"
    proxyPort = 9999
    pageAction = BaseTest().get_random_string(5)
    captcha_type = ReCaptchaV3TypeEnm.ReCaptchaV3Task

    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_params(self, proxy_type: str):
        ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            pageAction=self.pageAction,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        )

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_params_context(self, proxy_type: str):
        with ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
            pageAction=self.pageAction,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        ) as instance:
            pass

    """
    Failed tests
    """

    def test_no_website_key(self):
        with pytest.raises(TypeError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                pageAction=self.pageAction,
            )

    def test_no_website_url(self):
        with pytest.raises(TypeError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteKey=self.googlekey,
                pageAction=self.pageAction,
            )

    def test_no_page_action(self):
        with pytest.raises(ValidationError):
            ReCaptcha(
                api_key=self.API_KEY, captcha_type=self.captcha_type, websiteKey=self.googlekey, websiteURL=self.pageurl
            )
