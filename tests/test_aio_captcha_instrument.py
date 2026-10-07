from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.conftest import BaseTest
from python3_capsolver.core.base import CaptchaParams
from python3_capsolver.core.enum import CaptchaTypeEnm, EndpointPostfixEnm
from python3_capsolver.core.const import REQUEST_URL
from python3_capsolver.core.aio_captcha_instrument import AIOCaptchaInstrument

API_KEY_STUB = "unit-test-api-key-000000000000000000000000"
CREATE_TASK_URL = "https://unit.test/createTask"
GET_TASK_RESULT_URL = "https://unit.test/getTaskResult"


def create_captcha_params() -> CaptchaParams:
    """
    Build params pointing to a fake API host with zero sleep between polls:
    no real request can leave the mocked `aiohttp.ClientSession.post` boundary
    """
    return CaptchaParams(
        api_key=API_KEY_STUB,
        captcha_type=CaptchaTypeEnm.Control,
        sleep_time=0,
        request_url="https://unit.test/",
    )


def aio_response(payload=None, status: int = 200, reason: str = "unit test failure") -> MagicMock:
    """
    Build fake response for the `aiohttp` boundary, usable as async context manager.

    For non-parsable bodies (``payload is None``) any ``json()`` call raises -
    an error status must never be parsed as a success body
    """
    response = MagicMock()
    response.status = status
    response.reason = reason
    if payload is None:
        response.json = AsyncMock(side_effect=AssertionError("body of an error response must not be parsed"))
    else:
        response.json = AsyncMock(return_value=payload)
    response.__aenter__.return_value = response
    return response


class TestAIOCaptchaInstrument(BaseTest):
    """
    Mocked unit tests for AIOCaptchaInstrument
    """

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_returns_created_result_without_polling_when_task_is_ready(self, mock_post):
        mock_post.return_value = aio_response(
            {"errorId": 0, "taskId": "task-ready-1", "status": "ready", "solution": {"text": "wg6x"}}
        )

        result = await AIOCaptchaInstrument(captcha_params=create_captcha_params()).processing_captcha()

        assert result["errorId"] == 0
        assert result["status"] == "ready"
        assert result["taskId"] == "task-ready-1"
        assert result["solution"] == {"text": "wg6x"}
        # task was solved at creation - no `getTaskResult` polling must follow
        mock_post.assert_called_once()
        assert mock_post.call_args.args[0] == CREATE_TASK_URL
        assert mock_post.call_args.kwargs["json"]["task"] == {"type": "Control"}
        assert mock_post.call_args.kwargs["json"]["clientKey"] == API_KEY_STUB

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_polls_get_task_result_until_ready(self, mock_post):
        mock_post.side_effect = [
            aio_response({"errorId": 0, "taskId": "task-42", "status": "processing"}),
            aio_response({"errorId": 0, "taskId": "task-42", "status": "processing"}),
            aio_response({"errorId": 0, "taskId": "task-42", "status": "ready", "solution": {"text": "ab12"}}),
        ]

        result = await AIOCaptchaInstrument(captcha_params=create_captcha_params()).processing_captcha()

        assert result["errorId"] == 0
        assert result["status"] == "ready"
        assert result["solution"] == {"text": "ab12"}
        assert [call.args[0] for call in mock_post.call_args_list] == [
            CREATE_TASK_URL,
            GET_TASK_RESULT_URL,
            GET_TASK_RESULT_URL,
        ]
        # created taskId must be propagated to every polling request
        assert mock_post.call_args_list[1].kwargs["json"]["taskId"] == "task-42"
        assert mock_post.call_args_list[2].kwargs["json"]["taskId"] == "task-42"

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_returns_failed_result_when_polling_reports_failure(self, mock_post):
        mock_post.side_effect = [
            aio_response({"errorId": 0, "taskId": "task-42", "status": "processing"}),
            aio_response({"errorId": 1, "errorCode": "ERROR_TASK_NOT_FOUND", "status": "failed"}),
        ]

        result = await AIOCaptchaInstrument(captcha_params=create_captcha_params()).processing_captcha()

        assert result["errorId"] == 1
        assert result["status"] == "failed"
        assert result["errorCode"] == "ERROR_TASK_NOT_FOUND"
        assert len(mock_post.call_args_list) == 2

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_marks_result_failed_when_task_creation_is_rejected(self, mock_post):
        mock_post.return_value = aio_response(
            {"errorId": 1, "errorCode": "ERROR_KEY_DOES_NOT_EXIST", "errorDescription": "Client key is invalid"}
        )

        result = await AIOCaptchaInstrument(captcha_params=create_captcha_params()).processing_captcha()

        assert result["errorId"] == 1
        assert result["status"] == "failed"
        assert result["errorCode"] == "ERROR_KEY_DOES_NOT_EXIST"
        assert result["errorDescription"] == "Client key is invalid"
        # rejected creation must not trigger result polling
        mock_post.assert_called_once()

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_parses_error_payload_when_status_code_is_valid_error_status(self, mock_post):
        mock_post.return_value = aio_response({"errorId": 1, "errorCode": "ERROR_WRONG_USERKEY"}, status=400)

        result = await AIOCaptchaInstrument(captcha_params=create_captcha_params()).processing_captcha()

        assert result["status"] == "failed"
        assert result["errorCode"] == "ERROR_WRONG_USERKEY"

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_returns_unsolvable_default_when_server_never_finishes(self, mock_post):
        mock_post.side_effect = [aio_response({"errorId": 0, "taskId": "task-silent", "status": "processing"})] * 16

        result = await AIOCaptchaInstrument(captcha_params=create_captcha_params()).processing_captcha()

        assert result["errorId"] == 1
        assert result["errorCode"] == "ERROR_CAPTCHA_UNSOLVABLE"
        assert result["errorDescription"] == "Captcha not recognized"
        assert result["status"] == "failed"
        assert result["taskId"] == "task-silent"
        # 1 `createTask` + 15 polling attempts, then the instrument gives up
        assert len(mock_post.call_args_list) == 16

    @pytest.mark.parametrize("bad_status", [404, 500])
    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_raises_when_create_task_returns_invalid_status(self, mock_post, bad_status):
        mock_post.return_value = aio_response(status=bad_status, reason="Internal Server Error")

        with pytest.raises(ValueError):
            await AIOCaptchaInstrument(captcha_params=create_captcha_params()).processing_captcha()

        mock_post.assert_called_once()

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_raises_when_get_task_result_returns_invalid_status(self, mock_post):
        mock_post.side_effect = [
            aio_response({"errorId": 0, "taskId": "task-42", "status": "processing"}),
            aio_response(status=503, reason="Service Unavailable"),
        ]

        with pytest.raises(ValueError):
            await AIOCaptchaInstrument(captcha_params=create_captcha_params()).processing_captcha()

        assert len(mock_post.call_args_list) == 2

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_send_post_request_returns_decoded_payload(self, mock_post):
        mock_post.return_value = aio_response({"errorId": 0, "balance": 107.7})

        result = await AIOCaptchaInstrument.send_post_request(
            payload={"clientKey": API_KEY_STUB},
            url_postfix=EndpointPostfixEnm.GET_BALANCE,
        )

        assert result == {"errorId": 0, "balance": 107.7}
        assert mock_post.call_args.args[0] == f"{REQUEST_URL}/{EndpointPostfixEnm.GET_BALANCE.value}"
        assert mock_post.call_args.kwargs["json"] == {"clientKey": API_KEY_STUB}

    @patch("python3_capsolver.core.aio_captcha_instrument.aiohttp.ClientSession.post")
    async def test_send_post_request_raises_for_error_status(self, mock_post):
        mock_post.return_value = aio_response(status=403)

        with pytest.raises(ValueError):
            await AIOCaptchaInstrument.send_post_request(payload={"clientKey": API_KEY_STUB})

        mock_post.assert_called_once()
