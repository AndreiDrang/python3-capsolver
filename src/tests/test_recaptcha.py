import pytest
from pydantic import ValidationError

from src.tests.conftest import BaseTest
from python3_captchaai.recaptcha import ReCaptcha
from python3_captchaai.core.enums import ProxyType, CaptchaTypeEnm

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

    captcha_types = (CaptchaTypeEnm.ReCaptchaV2TaskProxyLess, CaptchaTypeEnm.ReCaptchaV2EnterpriseTaskProxyless)
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

    # TODO start use it, temporary Captcha not solving
    """def test_solve(self):
        resp = ReCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.googlekey,
        ).captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Ready
        assert resp.errorId is False
        assert resp.errorCode is None
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
        assert resp.errorId is False
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
        assert resp.errorId is False
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

    @pytest.mark.parametrize("captcha_type", captcha_types)
    async def test_aio_api_key_err(self, captcha_type: str):
        with pytest.raises(Exception):
            await ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
            ).aio_captcha_handler()

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_api_key_err(self, captcha_type: str):
        with pytest.raises(Exception):
            ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
            ).captcha_handler()


class TestReCaptchaV2(BaseTest):
    googlekey = GOOGLE_KEY
    pageurl = PAGE_URL
    proxyAddress = "0.0.0.0"
    proxyPort = 9999
    captcha_types = (CaptchaTypeEnm.ReCaptchaV2Task, CaptchaTypeEnm.ReCaptchaV2EnterpriseTask)

    """
    Success tests
    """

    @pytest.mark.parametrize("captcha_type", captcha_types)
    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
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
    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
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

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_no_proxy_type(self, captcha_type: str):
        with pytest.raises(ValidationError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
                proxyAddress=self.proxyAddress,
                proxyPort=self.proxyPort,
            )

    @pytest.mark.parametrize("captcha_type", captcha_types)
    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxy_address(self, proxy_type: str, captcha_type: str):
        with pytest.raises(ValidationError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
            )

    @pytest.mark.parametrize("captcha_type", captcha_types)
    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxy_port(self, proxy_type, captcha_type: str):
        with pytest.raises(ValidationError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
            )

    @pytest.mark.parametrize("captcha_type", captcha_types)
    async def test_aio_api_key_err(self, captcha_type: str):
        with pytest.raises(Exception):
            await ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
            ).aio_captcha_handler()

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_api_key_err(self, captcha_type: str):
        with pytest.raises(Exception):
            ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
            ).captcha_handler()


class TestReCaptchaV3ProxyLess(BaseTest):
    googlekey = GOOGLE_KEY
    pageurl = PAGE_URL

    pageAction = BaseTest().get_random_string(5)
    captcha_type = CaptchaTypeEnm.ReCaptchaV3TaskProxyless

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

    async def test_aio_api_key_err(self):
        with pytest.raises(Exception):
            await ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
                pageAction=self.pageAction,
            ).aio_captcha_handler()

    def test_api_key_err(self):
        with pytest.raises(Exception):
            ReCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
                pageAction=self.pageAction,
            ).captcha_handler()


class TestReCaptchaV3(BaseTest):
    googlekey = GOOGLE_KEY
    pageurl = PAGE_URL

    proxyAddress = "0.0.0.0"
    proxyPort = 9999
    pageAction = BaseTest().get_random_string(5)
    captcha_type = CaptchaTypeEnm.ReCaptchaV3Task

    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
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

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
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

    def test_no_proxy_type(self):
        with pytest.raises(ValidationError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
                pageAction=self.pageAction,
                proxyAddress=self.proxyAddress,
                proxyPort=self.proxyPort,
            )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxy_address(self, proxy_type: str):
        with pytest.raises(ValidationError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
                pageAction=self.pageAction,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
            )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxy_port(self, proxy_type):
        with pytest.raises(ValidationError):
            ReCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
                pageAction=self.pageAction,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
            )
