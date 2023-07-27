import base64

from tests.conftest import BaseTest
from python3_capsolver.core.enum import ResponseStatusEnm
from python3_capsolver.image_to_text import ImageToText
from python3_capsolver.core.serializer import CaptchaResponseSer

with open("tests/files/captcha_example.jpeg", "rb") as img_file:
    img_data = img_file.read()


class TestImageToText(BaseTest):
    image_body = base64.b64encode(img_data).decode("utf-8")
    """
    Success tests
    """

    def test_captcha_handler_exist(self):
        assert "captcha_handler" in ImageToText.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in ImageToText.__dict__.keys()

    def test_solve_image(self):
        resp = ImageToText(api_key=self.API_KEY).captcha_handler(body=self.image_body)
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Processing)
        assert resp.errorId in (False, True)
        assert resp.errorCode in (None, "ERROR_ZERO_BALANCE")
        assert resp.errorDescription in (None, "Your service balance is insufficient.")

    def test_solve_image_context(self):
        with ImageToText(api_key=self.API_KEY) as instance:
            resp = instance.captcha_handler(body=self.image_body)
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Processing)
        assert resp.errorId in (False, True)
        assert resp.errorCode in (None, "ERROR_ZERO_BALANCE")
        assert resp.errorDescription in (None, "Your service balance is insufficient.")

    async def test_aio_solve_image(self):
        resp = await ImageToText(api_key=self.API_KEY).aio_captcha_handler(body=self.image_body)
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Processing)
        assert resp.errorId in (False, True)
        assert resp.errorCode in (None, "ERROR_ZERO_BALANCE")
        assert resp.errorDescription in (None, "Your service balance is insufficient.")

    async def test_aio_solve_image_context(self):
        with ImageToText(api_key=self.API_KEY) as instance:
            resp = await instance.aio_captcha_handler(body=self.image_body)
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Processing)
        assert resp.errorId in (False, True)
        assert resp.errorCode in (None, "ERROR_ZERO_BALANCE")
        assert resp.errorDescription in (None, "Your service balance is insufficient.")

    """
    Failed tests
    """

    def test_captcha_handler_api_key_err(self):
        result = ImageToText(api_key=self.get_random_string(36)).captcha_handler(body=self.image_body)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution

    async def test_aio_captcha_handler_api_key_err(self):
        result = await ImageToText(api_key=self.get_random_string(36)).aio_captcha_handler(body=self.image_body)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution
