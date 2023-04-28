import pytest
from pydantic import ValidationError

from tests.conftest import BaseTest
from python3_capsolver.gee_test import GeeTest
from python3_capsolver.core.enum import ProxyType, CaptchaTypeEnm

PAGE_URL = "https://www.geetest.com/en/demo"
GT = "022397c99c9f646f6477822485f30404"
CHALLENGE = "a66f31a53a404af8d1f271eec5138aa1"
API_SUBDOMAIN = "api.geetest.com"

captcha_types = (CaptchaTypeEnm.GeetestTask, CaptchaTypeEnm.GeetestTaskProxyless)


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
                websiteURL=PAGE_URL,
                gt=GT,
            )

    def test_wrong_type_params(self):
        with pytest.raises(ValidationError):
            GeeTest(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.GeetestTask,
                websiteURL=PAGE_URL,
                gt=GT,
            ).captcha_handler(challenge=CHALLENGE)

    async def test_aio_wrong_type_params(self):
        with pytest.raises(ValidationError):
            await GeeTest(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.GeetestTask,
                websiteURL=PAGE_URL,
                gt=GT,
            ).aio_captcha_handler(challenge=CHALLENGE)

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            GeeTest(
                api_key=self.get_random_string(36),
                websiteURL="https://www.geetest.com/en/demo",
                gt="022397c99c9f646f6477822485f30404",
            )

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_no_gt_key(self, captcha_type: str):
        with pytest.raises(TypeError):
            GeeTest(api_key=self.API_KEY, captcha_type=captcha_type, websiteURL=PAGE_URL)

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_no_website_url(self, captcha_type: str):
        with pytest.raises(TypeError):
            GeeTest(api_key=self.API_KEY, captcha_type=captcha_type, gt=GT)


class TestGeeTestProxyLess(BaseTest):
    captcha_type = CaptchaTypeEnm.GeetestTaskProxyless
    """
    Success tests
    """

    def test_params(self):
        GeeTest(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteURL=PAGE_URL, gt=GT)

    def test_params_context(self):
        with GeeTest(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteURL=PAGE_URL, gt=GT) as instance:
            pass

    """
    Failed tests
    """

    async def test_aio_api_key_err(self):
        with pytest.raises(ValueError):
            await GeeTest(
                api_key=self.get_random_string(36), captcha_type=self.captcha_type, websiteURL=PAGE_URL, gt=GT
            ).aio_captcha_handler(challenge=CHALLENGE, geetestApiServerSubdomain="api.geetest.com")

    def test_api_key_err(self):
        with pytest.raises(ValueError):
            GeeTest(
                api_key=self.get_random_string(36), captcha_type=self.captcha_type, websiteURL=PAGE_URL, gt=GT
            ).captcha_handler(challenge=CHALLENGE, geetestApiServerSubdomain="api.geetest.com")


class TestGeeTest(BaseTest):
    captcha_type = CaptchaTypeEnm.GeetestTask

    proxyAddress = "0.0.0.0"
    proxyPort = 9999
    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_params(self, proxy_type: str):
        GeeTest(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_params_context(self, proxy_type: str):
        with GeeTest(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        ) as instance:
            pass

    """
    Failed tests
    """

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    async def test_aio_api_key_err(self, proxy_type: str):
        with pytest.raises(ValueError):
            await GeeTest(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=PAGE_URL,
                gt=GT,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
            ).aio_captcha_handler(challenge=CHALLENGE, geetestApiServerSubdomain="api.geetest.com")

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_api_key_err(self, proxy_type: str):
        with pytest.raises(ValueError):
            GeeTest(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=PAGE_URL,
                gt=GT,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
            ).captcha_handler(challenge=CHALLENGE, geetestApiServerSubdomain="api.geetest.com")
