import pytest

from tests.conftest import BaseTest
from python3_capsolver.binance import Binance
from python3_capsolver.core.enum import BinanceCaptchaTaskEnm


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
