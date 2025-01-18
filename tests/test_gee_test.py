from tests.conftest import BaseTest
from python3_capsolver.gee_test import GeeTest
from python3_capsolver.core.enum import CaptchaTypeEnm


class TestGeeTest(BaseTest):

    def test_captcha_handler_exist(self):
        instance = GeeTest(api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.GeeTestTaskProxyLess)
        assert "captcha_handler" in instance.__dir__()
        assert "aio_captcha_handler" in instance.__dir__()

    def test_api_key_err(self):
        result = GeeTest(
            api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.GeeTestTaskProxyLess
        ).captcha_handler(task_payload={"some": "data"})
        assert result["errorId"] == 1
        assert result["errorCode"] in ("ERROR_KEY_DENIED_ACCESS", "ERROR_INVALID_TASK_DATA")
        assert result["solution"] is None

    async def test_aio_api_key_err(self):
        result = await GeeTest(
            api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.GeeTestTaskProxyLess
        ).aio_captcha_handler(task_payload={"some": "data"})
        assert result["errorId"] == 1
        assert result["errorCode"] in ("ERROR_KEY_DENIED_ACCESS", "ERROR_INVALID_TASK_DATA")
        assert result["solution"] is None
