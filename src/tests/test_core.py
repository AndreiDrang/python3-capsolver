import pytest
from tenacity import AsyncRetrying
from urllib3.util.retry import Retry

from src.tests.conftest import BaseTest
from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enums import CaptchaTypeEnm
from python3_captchaai.core.config import RETRIES, ASYNC_RETRIES


class TestCore(BaseTest):
    """
    Success tests
    """

    def test_reties(self):
        assert isinstance(RETRIES, Retry)

    def test_async_reties(self):
        assert isinstance(ASYNC_RETRIES, AsyncRetrying)

    async def test_no_key_err(self):
        with pytest.raises(TypeError):
            BaseCaptcha(captcha_type=CaptchaTypeEnm.ImageToTextTask)

    async def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            BaseCaptcha(api_key=self.get_random_string(36))

    @pytest.mark.parametrize("api_len", [35, 37])
    def test_wrong_key_err(self, api_len: int):
        with pytest.raises(ValueError):
            BaseCaptcha(api_key=self.get_random_string(api_len), captcha_type=CaptchaTypeEnm.ImageToTextTask)

    @pytest.mark.parametrize("sleep_time", range(-2, 5))
    def test_wrong_sleep_time(self, sleep_time: int):
        with pytest.raises(ValueError):
            BaseCaptcha(
                api_key=self.get_random_string(36), sleep_time=sleep_time, captcha_type=CaptchaTypeEnm.ImageToTextTask
            )

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            BaseCaptcha(api_key=self.get_random_string(36), captcha_type=self.get_random_string(10))
