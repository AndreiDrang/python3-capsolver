import pytest

from src.tests.conftest import BaseTest
from python3_capsolver.kasada import Kasada
from python3_capsolver.core.enum import ProxyType

pageURL = "http://mywebsite.com/kasada"


class TestFunCaptchaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in Kasada.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in Kasada.__dict__.keys()


class TestKasada(BaseTest):

    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_params(self, proxy_type: str):
        Kasada(
            api_key=self.get_random_string(36),
            pageURL=pageURL,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
            proxyLogin=self.get_random_string(5),
            proxyPassword=self.get_random_string(5),
        )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_params_context(self, proxy_type: str):
        with Kasada(
            api_key=self.get_random_string(36),
            pageURL=pageURL,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
            proxyLogin=self.get_random_string(5),
            proxyPassword=self.get_random_string(5),
        ) as instance:
            pass

    """
    Failed tests
    """

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_err(self, proxy_type: str):
        with pytest.raises(ValueError):
            Kasada(
                api_key=self.get_random_string(36),
                pageURL=pageURL,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
                proxyLogin=self.get_random_string(5),
                proxyPassword=self.get_random_string(5),
            ).captcha_handler()

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    async def test_aio_err(self, proxy_type: str):
        with pytest.raises(ValueError):
            await Kasada(
                api_key=self.get_random_string(36),
                pageURL=pageURL,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
                proxyLogin=self.get_random_string(5),
                proxyPassword=self.get_random_string(5),
            ).aio_captcha_handler()

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_pageurl(self, proxy_type: str):
        with pytest.raises(TypeError):
            Kasada(
                api_key=self.get_random_string(36),
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
                proxyLogin=self.get_random_string(5),
                proxyPassword=self.get_random_string(5),
            )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxyaddress(self, proxy_type: str):
        with pytest.raises(TypeError):
            Kasada(
                api_key=self.get_random_string(36),
                pageURL=pageURL,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
                proxyLogin=self.get_random_string(5),
                proxyPassword=self.get_random_string(5),
            )

    def test_no_proxytype(self):
        with pytest.raises(TypeError):
            Kasada(
                api_key=self.get_random_string(36),
                pageURL=pageURL,
                proxyAddress=self.proxyAddress,
                proxyPort=self.proxyPort,
                proxyLogin=self.get_random_string(5),
                proxyPassword=self.get_random_string(5),
            )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxyport(self, proxy_type: str):
        with pytest.raises(TypeError):
            Kasada(
                api_key=self.get_random_string(36),
                pageURL=pageURL,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
                proxyLogin=self.get_random_string(5),
                proxyPassword=self.get_random_string(5),
            )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxylogin(self, proxy_type: str):
        with pytest.raises(TypeError):
            Kasada(
                api_key=self.get_random_string(36),
                pageURL=pageURL,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
                proxyPassword=self.get_random_string(5),
            )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxypassword(self, proxy_type: str):
        with pytest.raises(TypeError):
            Kasada(
                api_key=self.get_random_string(36),
                pageURL=pageURL,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
                proxyLogin=self.get_random_string(5),
            )
