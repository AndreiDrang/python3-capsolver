import pytest

from tests.conftest import BaseTest
from python3_capsolver.aws_waf import AwsWaf
from python3_capsolver.core.enum import CaptchaTypeEnm, ResponseStatusEnm


class TestAwsWafBase(BaseTest):
    captcha_types = (
        CaptchaTypeEnm.AwsWafClassification,
        CaptchaTypeEnm.AntiAwsWafTask,
        CaptchaTypeEnm.AntiAwsWafTaskProxyLess,
    )

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_captcha_handler_exist(self, captcha_type):
        instance = AwsWaf(api_key=self.get_random_string(36), captcha_type=captcha_type)
        assert "captcha_handler" in instance.__dir__()
        assert "aio_captcha_handler" in instance.__dir__()

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_api_key_err(self, captcha_type):
        result = AwsWaf(api_key=self.get_random_string(36), captcha_type=captcha_type).captcha_handler(
            task_payload={"some": "data"}
        )
        assert result["errorId"] == 1
        assert result["errorCode"] in ("ERROR_INVALID_TASK_DATA", "ERROR_KEY_DENIED_ACCESS")
        assert result["solution"] is None

    @pytest.mark.parametrize("captcha_type", captcha_types)
    async def test_aio_api_key_err(self, captcha_type):
        result = await AwsWaf(api_key=self.get_random_string(36), captcha_type=captcha_type).aio_captcha_handler(
            task_payload={"some": "data"}
        )
        assert result["errorId"] == 1
        assert result["errorCode"] in ("ERROR_INVALID_TASK_DATA", "ERROR_KEY_DENIED_ACCESS")
        assert result["solution"] is None


class TestAwsWafClassification(BaseTest):
    toycarcity_image = "tests/files/aws_waf_class_toycarcity.png"

    def test_success(self):
        result = AwsWaf(api_key=self.API_KEY, captcha_type=CaptchaTypeEnm.AwsWafClassification).captcha_handler(
            task_payload={
                "images": [self.read_image_as_str(file_path=self.toycarcity_image)],
                "question": "aws:toycarcity:carcity",
            }
        )
        assert result["errorId"] == 0
        assert result["errorCode"] is None
        assert isinstance(result["solution"], dict)
        assert result["status"] == ResponseStatusEnm.Ready.value
        assert result["taskId"] is not ""

    def test_api_key_err(self):
        result = AwsWaf(
            api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.AwsWafClassification
        ).captcha_handler(
            task_payload={
                "images": [self.read_image_as_str()],
                "question": "aws:toycarcity:carcity",
            }
        )
        assert result["errorId"] == 1
        assert result["errorCode"] == "ERROR_KEY_DENIED_ACCESS"
        assert result["solution"] is None

    async def test_aio_api_key_err(self):
        result = await AwsWaf(
            api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.AwsWafClassification
        ).aio_captcha_handler(
            task_payload={
                "images": [self.read_image_as_str()],
                "question": "aws:toycarcity:carcity",
            }
        )
        assert result["errorId"] == 1
        assert result["errorCode"] == "ERROR_KEY_DENIED_ACCESS"
        assert result["solution"] is None


class TestAntiAwsWafTaskProxyLess(BaseTest):

    def test_api_key_err(self):
        result = AwsWaf(
            api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.AntiAwsWafTaskProxyLess
        ).captcha_handler(
            task_payload={
                "websiteURL": "https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest",
                "awsKey": "AQIDAHjcYu/GjX+QlghicBg......shMIKvZswZemrVVqA==",
                "awsIv": "CgAAFDIlckAAAAid",
                "awsContext": "7DhQfG5CmoY90ZdxdHCi8WtJ3z......njNKULdcUUVEtxTk=",
                "awsChallengeJS": "https://41bcdd4fb3cb.610cd090.us-east-1.token.awswaf.com/41bcdd4fb3cb/0d21de737ccb/cd77baa6c832/challenge.js",
            }
        )
        assert result["errorId"] == 1
        assert result["errorCode"] == "ERROR_KEY_DENIED_ACCESS"
        assert result["solution"] is None

    async def test_aio_api_key_err(self):
        result = await AwsWaf(
            api_key=self.get_random_string(36), captcha_type=CaptchaTypeEnm.AntiAwsWafTaskProxyLess
        ).aio_captcha_handler(
            task_payload={
                "websiteURL": "https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest",
                "awsKey": "AQIDAHjcYu/GjX+QlghicBg......shMIKvZswZemrVVqA==",
                "awsIv": "CgAAFDIlckAAAAid",
                "awsContext": "7DhQfG5CmoY90ZdxdHCi8WtJ3z......njNKULdcUUVEtxTk=",
                "awsChallengeJS": "https://41bcdd4fb3cb.610cd090.us-east-1.token.awswaf.com/41bcdd4fb3cb/0d21de737ccb/cd77baa6c832/challenge.js",
            }
        )
        assert result["errorId"] == 1
        assert result["errorCode"] == "ERROR_KEY_DENIED_ACCESS"
        assert result["solution"] is None
