import pytest

from tests.conftest import BaseTest
from python3_capsolver.core.enum import ResponseStatusEnm
from python3_capsolver.core.serializer import CaptchaResponseSer
from python3_capsolver.datadome_slider import DatadomeSlider

websiteURL = "https://www.some-url.com/"
captchaUrl = "https://www.some-url.com/to-page-with-captcha"


class TestDatadomeSliderBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in DatadomeSlider.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in DatadomeSlider.__dict__.keys()


class TestDatadomeSlider(BaseTest):
    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_params(self, proxy_type: str):
        DatadomeSlider(
            api_key=self.API_KEY,
            websiteURL=websiteURL,
            captchaUrl=captchaUrl,
            userAgent=self.get_random_string(36),
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        )

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_params_context(self, proxy_type: str):
        with DatadomeSlider(
            api_key=self.API_KEY,
            websiteURL=websiteURL,
            captchaUrl=captchaUrl,
            userAgent=self.get_random_string(36),
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        ) as instance:
            pass

    """
    Failed tests
    """

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    async def test_aio_proxy_err(self, proxy_type: str):
        resp = await DatadomeSlider(
            api_key=self.API_KEY,
            websiteURL=websiteURL,
            captchaUrl=captchaUrl,
            userAgent=self.get_random_string(36),
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        ).aio_captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId == 1
        assert resp.errorCode == "ERROR_PROXY_CONNECT_REFUSED"
        assert resp.solution is None

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
    def test_proxy_err(self, proxy_type: str):
        resp = DatadomeSlider(
            api_key=self.API_KEY,
            websiteURL=websiteURL,
            captchaUrl=captchaUrl,
            userAgent=self.get_random_string(36),
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        ).captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId == 1
        assert resp.errorCode == "ERROR_PROXY_CONNECT_REFUSED"
        assert resp.solution is None
