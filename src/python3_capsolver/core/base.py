from typing import Any, Dict

from .enum import CaptchaTypeEnm
from .const import REQUEST_URL
from .serializer import TaskSer, RequestCreateTaskSer, RequestGetTaskResultSer
from .context_instr import AIOContextManager, SIOContextManager
from .captcha_instrument import CaptchaInstrumentBase
from .aio_captcha_instrument import AIOCaptchaInstrument
from .sio_captcha_instrument import SIOCaptchaInstrument

__all__ = ("CaptchaParams",)


class CaptchaParams(SIOContextManager, AIOContextManager):
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: CaptchaTypeEnm,
        sleep_time: int = 5,
        request_url: str = REQUEST_URL,
    ):
        # assign args to validator
        self.create_task_payload = RequestCreateTaskSer(clientKey=api_key)
        # `task` body for task creation payload
        self.task_params = TaskSer(type=captcha_type.value).to_dict()
        # prepare `get task result` payload
        self.get_result_params = RequestGetTaskResultSer(clientKey=api_key)
        self.request_url = request_url
        self._captcha_handling_instrument = CaptchaInstrumentBase()
        self.sleep_time = sleep_time

    def captcha_handler(self, task_payload: Dict) -> Dict[str, Any]:
        """
        Synchronous method for captcha solving

        Args:
            task_payload: Some additional parameters that will be used in creating the task
                            and will be passed to the payload under ``task`` key.
                            Like ``websiteURL``, ``image``, ``proxyPassword``, ``websiteKey`` and etc.
                            more info in service docs

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        self.task_params.update(task_payload)
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.processing_captcha()

    async def aio_captcha_handler(self, task_payload: Dict) -> Dict[str, Any]:
        """
        Asynchronous method for captcha solving

        Args:
            task_payload: Some additional parameters that will be used in creating the task
                            and will be passed to the payload under ``task`` key.
                            Like ``websiteURL``, ``image``, ``proxyPassword``, ``websiteKey`` and etc.
                            more info in service docs

        Returns:
            Dict with full server response

        Notes:
            Check class docstirng for more info
        """
        self.task_params.update(task_payload)
        self._captcha_handling_instrument = AIOCaptchaInstrument(captcha_params=self)
        return await self._captcha_handling_instrument.processing_captcha()
