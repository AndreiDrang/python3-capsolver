import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from tests.conftest import BaseTest
from python3_capsolver.control import Control


class TestControl(BaseTest):
    """
    Success tests
    """

    def test_get_balance_exist(self):
        assert "get_balance" in Control.__dict__.keys()
        assert "aio_get_balance" in Control.__dict__.keys()

    def test_get_balance(self):
        result = Control(api_key=self.API_KEY).get_balance()
        assert isinstance(result, dict)
        assert result["errorId"] == 0
        assert result["balance"] != 0.0

    async def test_aio_get_balance(self):
        result = await Control(api_key=self.API_KEY).aio_get_balance()
        assert isinstance(result, dict)
        assert result["errorId"] == 0
        assert result["balance"] != 0.0

    """
    Failed tests
    """

    def test_get_balance_api_key_err(self):
        with pytest.raises(ValueError):
            Control(api_key=self.get_random_string(36)).get_balance()

    async def test_aio_get_balance_api_key_err(self):
        with pytest.raises(ValueError):
            await Control(api_key=self.get_random_string(36)).aio_get_balance()


class TestControlMock(BaseTest):
    """
    Mocked Unit tests for Control class
    """

    @patch("python3_capsolver.core.sio_captcha_instrument.requests.Session.post")
    def test_create_task(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"errorId": 0, "taskId": "test-task-id"}
        mock_post.return_value = mock_response

        control = Control(api_key="test-key")
        result = control.create_task({"type": "ImageToTextTask", "body": "base64..."})

        assert result["taskId"] == "test-task-id"
        assert result["errorId"] == 0
        mock_post.assert_called_once()

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_aio_create_task(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(
            return_value={"errorId": 0, "taskId": "test-task-id"}
        )
        # Mock async context manager
        mock_resp.__aenter__.return_value = mock_resp
        mock_post.return_value = mock_resp

        control = Control(api_key="test-key")
        result = await control.aio_create_task(
            {"type": "ImageToTextTask", "body": "base64..."}
        )

        assert result["taskId"] == "test-task-id"
        assert result["errorId"] == 0

    @patch("python3_capsolver.core.sio_captcha_instrument.requests.Session.post")
    def test_get_task_result(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "errorId": 0,
            "status": "ready",
            "solution": {"text": "abc"},
        }
        mock_post.return_value = mock_response

        control = Control(api_key="test-key")
        result = control.get_task_result(task_id="test-id")

        assert result["status"] == "ready"
        assert result["solution"]["text"] == "abc"

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_aio_get_task_result(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(
            return_value={
                "errorId": 0,
                "status": "ready",
                "solution": {"text": "abc"},
            }
        )
        mock_resp.__aenter__.return_value = mock_resp
        mock_post.return_value = mock_resp

        control = Control(api_key="test-key")
        result = await control.aio_get_task_result(task_id="test-id")

        assert result["status"] == "ready"
        assert result["solution"]["text"] == "abc"

    @patch("python3_capsolver.core.sio_captcha_instrument.requests.Session.post")
    def test_get_token(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"errorId": 0, "taskId": "token-task-id"}
        mock_post.return_value = mock_response

        control = Control(api_key="test-key")
        result = control.get_token(
            {"type": "ReCaptchaV3TaskProxyLess", "websiteURL": "..."}
        )

        assert result["taskId"] == "token-task-id"

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_aio_get_token(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(
            return_value={"errorId": 0, "taskId": "token-task-id"}
        )
        mock_resp.__aenter__.return_value = mock_resp
        mock_post.return_value = mock_resp

        control = Control(api_key="test-key")
        result = await control.aio_get_token(
            {"type": "ReCaptchaV3TaskProxyLess", "websiteURL": "..."}
        )

        assert result["taskId"] == "token-task-id"

    @patch("python3_capsolver.core.sio_captcha_instrument.requests.Session.post")
    def test_feedback_task(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"errorId": 0, "message": "okay"}
        mock_post.return_value = mock_response

        control = Control(api_key="test-key")
        result = control.feedback_task(
            task_id="test-id", result_payload={"invalid": True}
        )

        assert result["message"] == "okay"

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_aio_feedback_task(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value={"errorId": 0, "message": "okay"})
        mock_resp.__aenter__.return_value = mock_resp
        mock_post.return_value = mock_resp

        control = Control(api_key="test-key")
        result = await control.aio_feedback_task(
            task_id="test-id", result_payload={"invalid": True}
        )

        assert result["message"] == "okay"
