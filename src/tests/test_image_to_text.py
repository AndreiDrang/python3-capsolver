import os
import base64
import logging

import pytest

from src.tests.conftest import BaseTest
from python3_captchaai.core.enums import ResponseStatusEnm
from python3_captchaai.image_to_text import ImageToText
from python3_captchaai.core.serializer import CaptchaResponseSer

print(os.getcwd())
logging.warning(os.getcwd())
with open("tests/files/captcha_example.jpeg", "rb") as img_file:
    img_data = img_file.read()


class TestControl(BaseTest):
    image_body = base64.b64encode(img_data).decode("utf-8")
    """
    Success tests
    """

    def test_get_balance_exist(self):
        assert "captcha_handler" in ImageToText.__dict__.keys()

    def test_aio_get_balance_exist(self):
        assert "aio_captcha_handler" in ImageToText.__dict__.keys()

    def test_solve_image(self):
        resp = ImageToText(api_key=self.API_KEY).captcha_handler(body=self.image_body)
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.state == ResponseStatusEnm.Ready
        assert resp.errorId is False
        assert resp.ErrorCode is None
        assert resp.errorDescription is None

    async def test_aio_solve_image(self):
        resp = await ImageToText(api_key=self.API_KEY).aio_captcha_handler(body=self.image_body)
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.state == ResponseStatusEnm.Ready
        assert resp.errorId is False
        assert resp.ErrorCode is None
        assert resp.errorDescription is None

    """
    Failed tests
    """

    def test_get_balance_api_key_err(self):
        with pytest.raises(Exception):
            ImageToText(api_key=self.get_random_string(36)).captcha_handler(body=self.image_body)

    async def test_aio_get_balance_api_key_err(self):
        with pytest.raises(Exception):
            await ImageToText(api_key=self.get_random_string(36)).aio_captcha_handler(body=self.image_body)
