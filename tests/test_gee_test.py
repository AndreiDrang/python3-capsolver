import pytest

from tests.conftest import BaseTest
from python3_capsolver.gee_test import GeeTest
from python3_capsolver.core.enum import GeeTestCaptchaTypeEnm

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
                captcha_type="test",
                websiteURL=PAGE_URL,
                gt=GT,
                challenge=CHALLENGE,
                geetestApiServerSubdomain="api.geetest.com",
            )

    def test_wrong_type_params(self):
        with pytest.raises(ValueError):
            GeeTest(
                api_key=self.get_random_string(36),
                captcha_type="test",
                websiteURL=PAGE_URL,
                gt=GT,
                challenge=CHALLENGE,
                geetestApiServerSubdomain="api.geetest.com",
            ).captcha_handler()

    async def test_aio_wrong_type_params(self):
        with pytest.raises(ValueError):
            await GeeTest(
                api_key=self.get_random_string(36),
                captcha_type="test",
                websiteURL=PAGE_URL,
                gt=GT,
                challenge=CHALLENGE,
            ).aio_captcha_handler()

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            GeeTest(
                api_key=self.get_random_string(36),
                websiteURL="https://www.geetest.com/en/demo",
                gt="022397c99c9f646f6477822485f30404",
                challenge=CHALLENGE,
            )

    @pytest.mark.parametrize("captcha_type", GeeTestCaptchaTypeEnm.list_values())
    def test_no_gt_key(self, captcha_type: str):
        with pytest.raises(TypeError):
            GeeTest(api_key=self.API_KEY, captcha_type=captcha_type, websiteURL=PAGE_URL)

    @pytest.mark.parametrize("captcha_type", GeeTestCaptchaTypeEnm.list_values())
    def test_no_website_url(self, captcha_type: str):
        with pytest.raises(TypeError):
            GeeTest(api_key=self.API_KEY, captcha_type=captcha_type, gt=GT)

    @pytest.mark.parametrize("captcha_type", GeeTestCaptchaTypeEnm.list_values())
    def test_no_challenge(self, captcha_type: str):
        with pytest.raises(TypeError):
            GeeTest(
                api_key=self.get_random_string(36),
                websiteURL="https://www.geetest.com/en/demo",
                gt="022397c99c9f646f6477822485f30404",
            )


class TestGeeTestProxyLess(BaseTest):
    captcha_type = GeeTestCaptchaTypeEnm.GeeTestTaskProxyLess
    """
    Success tests
    """

    def test_params(self):
        GeeTest(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            challenge=CHALLENGE,
        )

    def test_params_context(self):
        with GeeTest(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            challenge=CHALLENGE,
        ) as instance:
            pass

    """
    Failed tests
    """

    async def test_aio_api_key_err(self):
        result = await GeeTest(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            challenge=CHALLENGE,
            geetestApiServerSubdomain="api.geetest.com",
        ).aio_captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution

    def test_api_key_err(self):
        result = GeeTest(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            challenge=CHALLENGE,
            geetestApiServerSubdomain="api.geetest.com",
        ).captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution


class TestGeeTest(BaseTest):
    captcha_type = GeeTestCaptchaTypeEnm.GeeTestTask

    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_params(self, proxy_type: str):
        GeeTest(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            challenge=CHALLENGE,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        )

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_params_context(self, proxy_type: str):
        with GeeTest(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            challenge=CHALLENGE,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        ) as instance:
            pass

    """
    Failed tests
    """

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    async def test_aio_api_key_err(self, proxy_type: str):
        result = await GeeTest(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
            challenge=CHALLENGE,
            geetestApiServerSubdomain="api.geetest.com",
        ).aio_captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_api_key_err(self, proxy_type: str):
        result = GeeTest(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=PAGE_URL,
            gt=GT,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
            challenge=CHALLENGE,
            geetestApiServerSubdomain="api.geetest.com",
        ).captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution
