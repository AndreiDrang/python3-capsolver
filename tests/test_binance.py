import pytest

from tests.conftest import BaseTest
from python3_capsolver.binance import Binance
from python3_capsolver.core.enum import BinanceCaptchaTaskEnm
from python3_capsolver.core.serializer import CaptchaResponseSer


class TestBinanceBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in Binance.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in Binance.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            Binance(
                api_key=self.get_random_string(36),
                captcha_type="test",
                websiteURL=self.get_random_string(36),
                validateId=self.get_random_string(36),
            )

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            Binance(
                api_key=self.get_random_string(36),
                websiteURL=self.get_random_string(36),
                validateId=self.get_random_string(36),
            )

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            Binance(
                api_key=self.get_random_string(36),
                captcha_type=BinanceCaptchaTaskEnm.BinanceCaptchaTask,
                validateId=self.get_random_string(36),
            )

    def test_no_validateId(self):
        with pytest.raises(TypeError):
            Binance(
                api_key=self.get_random_string(36),
                captcha_type=BinanceCaptchaTaskEnm.BinanceCaptchaTask,
                websiteURL=self.get_random_string(36),
            )


class TestBinanceCaptchaTaskBase(BaseTest):
    def test_instance(self):
        instance = Binance(
            api_key=self.API_KEY,
            captcha_type=BinanceCaptchaTaskEnm.BinanceCaptchaTask,
            websiteURL="https://www.milanuncios.com/",
            validateId="3621a4fef82f4ab4a00e8b07465761c5",
        )

    def test_solve(self):
        instance = Binance(
            api_key=self.API_KEY,
            captcha_type=BinanceCaptchaTaskEnm.BinanceCaptchaTask,
            websiteURL="https://www.milanuncios.com/",
            validateId="3621a4fef82f4ab4a00e8b07465761c5",
            **{"proxyType": "socks5", "proxyAddress": "72.217.216.239", "proxyPort": 4145},
        )
        result = instance.captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_PROXY_CONNECT_REFUSED"

    async def test_aio_solve(self):
        instance = Binance(
            api_key=self.API_KEY,
            captcha_type=BinanceCaptchaTaskEnm.BinanceCaptchaTask,
            websiteURL="https://www.milanuncios.com/",
            validateId="3621a4fef82f4ab4a00e8b07465761c5",
            **{"proxyType": "socks5", "proxyAddress": "72.217.216.239", "proxyPort": 4145},
        )
        result = await instance.aio_captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_PROXY_CONNECT_REFUSED"
