from typing import Dict

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm, EndpointPostfixEnm
from .core.aio_captcha_instrument import AIOCaptchaInstrument
from .core.sio_captcha_instrument import SIOCaptchaInstrument

__all__ = ("Control",)


class Control(CaptchaParams):
    """
    The class is used to work with Capsolver control methods.

    Args:
        api_key: Capsolver API key

    Notes:
        https://docs.capsolver.com/en/guide/api-getbalance/

        https://docs.capsolver.com/en/guide/api-gettaskresult/

        https://docs.capsolver.com/en/guide/api-createtask/

        https://docs.capsolver.com/en/guide/api-getToken/
    """

    def __init__(
        self,
        api_key: str,
    ):
        super().__init__(api_key=api_key, captcha_type=CaptchaTypeEnm.Control)

    def get_balance(self) -> dict:
        """
        Synchronous method to view the balance

        Examples:
            >>> from python3_capsolver.control import Control
            >>> Control(api_key="CAI-1324...").get_balance()
            {'balance': 48.6361, 'errorId': 0, 'packages': []}

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=EndpointPostfixEnm.GET_BALANCE,
            payload={"clientKey": self.create_task_payload.clientKey},
        )

    async def aio_get_balance(self) -> dict:
        """
        Asynchronous method to view the balance

        Examples:
            >>> import asyncio
            >>> from python3_capsolver.control import Control
            >>> asyncio.run(Control(api_key="CAI-1324...").aio_get_balance())
            {'balance': 48.6361, 'errorId': 0, 'packages': []}

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=EndpointPostfixEnm.GET_BALANCE,
            payload={"clientKey": self.create_task_payload.clientKey},
        )

    def create_task(self, task_payload: Dict) -> dict:
        """
        Synchronous method to send custom ``createTask`` request.

        This is the custom analog for prepared captcha solving classes.
        With this method u can create task with custom type and get
        response with task solution or task ID (depends on task type).
        The main difference with ``captcha_handler`` methods
        - there is no retries logic and other sugar.

        Args:
            task_payload: Some additional parameters that will be used in creating the task
                            and will be passed to the payload under ``task`` key.
                            Like ``websiteURL``, ``image``, ``proxyPassword``, ``websiteKey`` and etc.
                            more info in service docs

        Examples:
            >>> from python3_capsolver.control import Control
            >>> Control(api_key="CAI-1324...").get_task_result(
            ...                             task_payload={
            ...                                 "type": "VisionEngine",
            ...                                 "image": "base64_image_body",
            ...                                 "question": "click on the object",
            ...                                 "module": "space_detection",
            ...                             }
            ...                     )
            {
                "errorId": 0,
                "errorCode":"None",
                "errorDescription":"None",
                "taskId": "db0a3153-xxxx",
                "status":"ready",
                "solution": {
                    "userAgent": "xxx",
                    "gRecaptchaResponse": "03AGdBq25SxXT-pmSeBXjzScW-xxxx"
                },
            }

        Returns:
            Dict with full server response

        Notes:
            https://docs.capsolver.com/en/guide/api-createtask/
        """
        self.task_params.update(task_payload)
        self.create_task_payload.task = self.task_params
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=EndpointPostfixEnm.CREATE_TASK,
            payload=self.create_task_payload.to_dict(),
        )

    async def aio_create_task(self, task_payload: Dict) -> dict:
        """
        Asynchronous method to send custom ``createTask`` request.

        This is the custom analog for prepared captcha solving classes.
        With this method u can create task with custom type and get
        response with task solution or task ID (depends on task type).
        The main difference with ``captcha_handler`` methods
        - there is no retries logic and other sugar.

        Args:
            task_payload: Some additional parameters that will be used in creating the task
                            and will be passed to the payload under ``task`` key.
                            Like ``websiteURL``, ``image``, ``proxyPassword``, ``websiteKey`` and etc.
                            more info in service docs

        Examples:
            >>> import asyncio
            >>> from python3_capsolver.control import Control
            >>> asyncio.run(Control(api_key="CAI-1324...")
            ...                 .aio_create_task(
            ...                             task_payload={
            ...                                 "type": "VisionEngine",
            ...                                 "image": "base64_image_body",
            ...                                 "question": "click on the unique object",
            ...                                 "module": "space_detection",
            ...                             }
            ...                     ))
            {
                "errorId": 0,
                "errorCode":"None",
                "errorDescription":"None",
                "taskId": "db0a3153-xxxx",
                "status":"ready",
                "solution": {
                    "userAgent": "xxx",
                    "gRecaptchaResponse": "03AGdBq25SxXT-pmSeBXjzScW-xxxx"
                },
            }

        Returns:
            Dict with full server response

        Notes:
            https://docs.capsolver.com/en/guide/api-createtask/
        """
        self.task_params.update(task_payload)
        self.create_task_payload.task = self.task_params
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=EndpointPostfixEnm.CREATE_TASK,
            payload=self.create_task_payload.to_dict(),
        )

    def get_task_result(self, task_id: str) -> dict:
        """
        Synchronous method to send ``getTaskResult`` request

        Args:
            task_id: Task ID

        Examples:
            >>> from python3_capsolver.control import Control
            >>> Control(api_key="CAI-1324...").get_task_result(task_id="db0a3153-xxxx")
            {
                "errorId": 0,
                "errorCode":"None",
                "errorDescription":"None",
                "taskId": "db0a3153-xxxx",
                "status":"ready",
                "solution": {
                    "userAgent": "xxx",
                    "gRecaptchaResponse": "03AGdBq25SxXT-pmSeBXjzScW-xxxx"
                },
            }

        Returns:
            Dict with full server response

        Notes:
            https://docs.capsolver.com/en/guide/api-gettaskresult/
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=EndpointPostfixEnm.GET_TASK_RESULT,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": task_id},
        )

    async def aio_get_task_result(self, task_id: str) -> dict:
        """
        Synchronous method to send ``getTaskResult`` request

        Args:
            task_id: Task ID

        Examples:
            >>> import asyncio
            >>> from python3_capsolver.control import Control
            >>> asyncio.run(Control(api_key="CAI-1324...")
            ...                     .aio_get_task_result(task_id="db0a3153-xxxx"))
            {
                "errorId": 0,
                "errorCode":"None",
                "errorDescription":"None",
                "taskId": "db0a3153-xxxx",
                "status":"ready",
                "solution": {
                    "userAgent": "xxx",
                    "gRecaptchaResponse": "03AGdBq25SxXT-pmSeBXjzScW-xxxx"
                },
            }

        Returns:
            Dict with full server response

        Notes:
            https://docs.capsolver.com/en/guide/api-gettaskresult/
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=EndpointPostfixEnm.GET_TASK_RESULT,
            payload={"clientKey": self.create_task_payload.clientKey, "taskId": task_id},
        )

    def get_token(self, task_payload: Dict) -> dict:
        """
        Synchronous method to send custom ``getToken`` request.

        Args:
            task_payload: Some additional parameters that will be used in creating the task
                            and will be passed to the payload under ``task`` key.
                            Like ``websiteURL``, ``image``, ``proxyPassword``, ``websiteKey`` and etc.
                            more info in service docs

        Examples:
            >>> from python3_capsolver.control import Control
            >>> Control(api_key="CAI-1324...").get_token(
            ...                             task_payload={
            ...                                 "type": "ReCaptchaV3TaskProxyLess",
            ...                                 "websiteURL": "https://demo.com/",
            ...                                 "websiteKey": "6LcpsXsnAAAbbAcxxxx"
            ...                             }
            ...                     )
            {
                "errorId": 0,
                "errorCode":"None",
                "errorDescription":"None",
                "taskId": "db0a3153-xxxx",
                "status":"ready",
                "solution": {
                    "gRecaptchaResponse": "03AGdBq25SxXT-pmSeBXjzScW-xxxx"
                },
            }

        Returns:
            Dict with full server response

        Notes:
            https://docs.capsolver.com/en/guide/api-getToken/
        """
        self.task_params.update(task_payload)
        self.create_task_payload.task = self.task_params
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=EndpointPostfixEnm.GET_TOKEN,
            payload=self.create_task_payload.to_dict(),
        )

    async def aio_get_token(self, task_payload: Dict) -> dict:
        """
        Asynchronous method to send custom ``getToken`` request.

        Args:
            task_payload: Some additional parameters that will be used in creating the task
                            and will be passed to the payload under ``task`` key.
                            Like ``websiteURL``, ``image``, ``proxyPassword``, ``websiteKey`` and etc.
                            more info in service docs

        Examples:
            >>> import asyncio
            >>> from python3_capsolver.control import Control
            >>> asyncio.run(Control(api_key="CAI-1324...")
            ...                 .aio_get_token(
            ...                             task_payload={
            ...                                 "type": "ReCaptchaV3TaskProxyLess",
            ...                                 "websiteURL": "https://demo.com/",
            ...                                 "websiteKey": "6LcpsXsnAAAbbAcxxxx"
            ...                             }
            ...                     ))
            {
                "errorId": 0,
                "errorCode":"None",
                "errorDescription":"None",
                "taskId": "db0a3153-xxxx",
                "status":"ready",
                "solution": {
                    "gRecaptchaResponse": "03AGdBq25SxXT-pmSeBXjzScW-xxxx"
                },
            }

        Returns:
            Dict with full server response

        Notes:
            https://docs.capsolver.com/en/guide/api-getToken/
        """
        self.task_params.update(task_payload)
        self.create_task_payload.task = self.task_params
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=EndpointPostfixEnm.GET_TOKEN,
            payload=self.create_task_payload.to_dict(),
        )

    def feedback_task(self, task_id: str, result_payload: Dict) -> dict:
        """
        Synchronous method to send custom ``feedbackTask`` request.

        Args:
            task_id: Task ID to report
            result_payload: Some additional parameters that will be used in creating the task
                            and will be passed to the payload under ``result`` key.
                            Like ``invalid``, ``code``, ``message`` and etc.
                            more info in service docs

        Examples:
            >>> from python3_capsolver.control import Control
            >>> Control(api_key="CAI-1324...").feedback_task(
            ...                             task_id="db0a3153-xxxx",
            ...                             result_payload={
            ...                                 "invalid": True,
            ...                                 "code": 1001,
            ...                                 "message": "invalid token"
            ...                             }
            ...                     )
            {
                "errorId": 0,
                "errorCode":"None",
                "errorDescription":"None",
                "message": "okay"
            }

        Returns:
            Dict with full server response

        Notes:
            https://docs.capsolver.com/en/guide/api-feedback/
        """
        self.task_params.update(result_payload)
        dict_payload = self.create_task_payload.to_dict()
        dict_payload.update({"result": self.task_params, "taskId": task_id})

        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=EndpointPostfixEnm.GET_TOKEN,
            payload=dict_payload,
        )

    async def aio_feedback_task(self, task_id: str, result_payload: Dict) -> dict:
        """
        Asynchronous method to send custom ``feedbackTask`` request.

        Args:
            task_id: Task ID to report
            result_payload: Some additional parameters that will be used in creating the task
                            and will be passed to the payload under ``result`` key.
                            Like ``invalid``, ``code``, ``message`` and etc.
                            more info in service docs

        Examples:
            >>> import asyncio
            >>> from python3_capsolver.control import Control
            >>> asyncio.run(Control(api_key="CAI-1324...")
            ...                 .aio_feedback_task(
            ...                             task_id="db0a3153-xxxx",
            ...                             result_payload={
            ...                                 "invalid": True,
            ...                                 "code": 1001,
            ...                                 "message": "invalid token"
            ...                             }
            ...                     ))
            {
                "errorId": 0,
                "errorCode":"None",
                "errorDescription":"None",
                "message": "okay"
            }

        Returns:
            Dict with full server response

        Notes:
            https://docs.capsolver.com/en/guide/api-feedback/
        """
        self.task_params.update(result_payload)
        dict_payload = self.create_task_payload.to_dict()
        dict_payload.update({"result": self.task_params, "taskId": task_id})

        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=EndpointPostfixEnm.GET_TOKEN,
            payload=dict_payload,
        )
