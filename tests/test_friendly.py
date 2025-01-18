import pytest

from tests.conftest import BaseTest
from python3_capsolver.core.enum import CaptchaTypeEnm
from python3_capsolver.friendly_captcha import FriendlyCaptcha


class TestFriendlyCaptchaBase(BaseTest):
    captcha_types = (CaptchaTypeEnm.FriendlyCaptchaTaskProxyless,)

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_captcha_handler_exist(self, captcha_type):
        instance = FriendlyCaptcha(api_key=self.get_random_string(36), captcha_type=captcha_type)
        assert "captcha_handler" in instance.__dir__()
        assert "aio_captcha_handler" in instance.__dir__()

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_api_key_err(self, captcha_type):
        result = FriendlyCaptcha(api_key=self.get_random_string(36), captcha_type=captcha_type).captcha_handler(
            task_payload={"some": "data"}
        )
        assert result["errorId"] == 1
        assert result["errorCode"] in ("ERROR_KEY_DENIED_ACCESS", "ERROR_INVALID_TASK_DATA")
        assert result["solution"] is None

    @pytest.mark.parametrize("captcha_type", captcha_types)
    async def test_aio_api_key_err(self, captcha_type):
        result = await FriendlyCaptcha(
            api_key=self.get_random_string(36), captcha_type=captcha_type
        ).aio_captcha_handler(task_payload={"some": "data"})
        assert result["errorId"] == 1
        assert result["errorCode"] in ("ERROR_KEY_DENIED_ACCESS", "ERROR_INVALID_TASK_DATA")
        assert result["solution"] is None
