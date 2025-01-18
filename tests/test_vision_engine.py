from tests.conftest import BaseTest
from python3_capsolver.vision_engine import VisionEngine


class TestVisionEngineBase(BaseTest):
    def test_captcha_handler_exist(self):
        instance = VisionEngine(api_key=self.get_random_string(36))
        assert "captcha_handler" in instance.__dir__()
        assert "aio_captcha_handler" in instance.__dir__()

    def test_api_key_err(self):
        result = VisionEngine(api_key=self.get_random_string(36)).captcha_handler(task_payload={"some": "data"})
        assert result["errorId"] == 1
        assert result["errorCode"] in ("ERROR_KEY_DENIED_ACCESS", "ERROR_INVALID_TASK_DATA")
        assert result["solution"] is None

    async def test_aio_api_key_err(self):
        result = await VisionEngine(api_key=self.get_random_string(36)).aio_captcha_handler(
            task_payload={"some": "data"}
        )
        assert result["errorId"] == 1
        assert result["errorCode"] in ("ERROR_KEY_DENIED_ACCESS", "ERROR_INVALID_TASK_DATA")
        assert result["solution"] is None
