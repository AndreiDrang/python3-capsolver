import base64

from tests.conftest import BaseTest
from python3_capsolver.core.enum import ResponseStatusEnm
from python3_capsolver.image_to_text import ImageToText
from python3_capsolver.core.serializer import CaptchaResponseSer

with open("tests/files/captcha_example.jpeg", "rb") as img_file:
    img_data = img_file.read()


class TestImageToTextBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in ImageToText.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in ImageToText.__dict__.keys()


class TestImageToText(BaseTest):
    image_body = base64.b64encode(img_data).decode("utf-8")
    """
    Success tests
    """

    def test_solve_image(self):
        resp = ImageToText(api_key=self.API_KEY).captcha_handler(task_payload=dict(body=self.image_body))
        assert isinstance(resp, dict)
        assert CaptchaResponseSer(**resp)
        assert resp["status"] == ResponseStatusEnm.Ready.value
        assert resp["errorId"] == 0
        assert resp["errorCode"] is None
        assert resp["errorDescription"] is None
        assert isinstance(resp["solution"], dict)

    async def test_aio_solve_image(self):
        resp = await ImageToText(api_key=self.API_KEY).aio_captcha_handler(task_payload=dict(body=self.image_body))
        assert isinstance(resp, dict)
        assert CaptchaResponseSer(**resp)
        assert resp["status"] == ResponseStatusEnm.Ready.value
        assert resp["errorId"] == 0
        assert resp["errorCode"] is None
        assert resp["errorDescription"] is None
        assert isinstance(resp["solution"], dict)

    """
    Failed tests
    """

    def test_captcha_handler_api_key_err(self):
        result = ImageToText(api_key=self.get_random_string(36)).captcha_handler(
            task_payload=dict(body=self.image_body)
        )
        assert result["errorId"] == 1
        assert result["errorCode"] == "ERROR_KEY_DENIED_ACCESS"
        assert result["solution"] is None

    async def test_aio_captcha_handler_api_key_err(self):
        result = await ImageToText(api_key=self.get_random_string(36)).aio_captcha_handler(
            task_payload=dict(body=self.image_body)
        )
        assert result["errorId"] == 1
        assert result["errorCode"] == "ERROR_KEY_DENIED_ACCESS"
        assert result["solution"] is None
