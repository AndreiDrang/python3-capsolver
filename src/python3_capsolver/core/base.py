import asyncio
import logging
from urllib import parse

import aiohttp

from .enum import ResponseStatusEnm, EndpointPostfixEnm
from .const import REQUEST_URL, VALID_STATUS_CODES
from .utils import attempts_generator
from .serializer import CaptchaResponseSer, RequestCreateTaskSer, RequestGetTaskResultSer
from .context_instr import AIOContextManager, SIOContextManager
from .captcha_instrument import CaptchaInstrument

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
        sleep_time: int = 5,
        request_url: str = REQUEST_URL,
        **kwargs,
    ):
        # assign args to validator
        self.create_task_payload = RequestCreateTaskSer(clientKey=api_key)
        # `task` body for task creation payload
        self.task_params = {}
        # prepare `get task result` payload
        self.get_result_params = RequestGetTaskResultSer(clientKey=api_key)
        self.request_url = request_url
        self._captcha_handling_instrument = CaptchaInstrument()

    """
    Async part
    """

    async def _aio_processing_captcha(self) -> dict:
        self._prepare_task_payload()
        self.created_task_data = CaptchaResponseSer(**await self._aio_create_task())

        # if task created and already ready - return result
        if self.created_task_data.errorId == 0 and self.created_task_data.status == ResponseStatusEnm.Processing.value:
            return (await self._aio_get_result()).to_dict()
        return self.created_task_data.to_dict()

    async def _aio_create_task(self, url_postfix: str = EndpointPostfixEnm.CREATE_TASK.value) -> dict:
        """
        Function send the ASYNC request to service and wait for result
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    parse.urljoin(self.__request_url, url_postfix), json=self.create_task_payload.to_dict()
                ) as resp:
                    if resp.status in VALID_STATUS_CODES:
                        return await resp.json()
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise

    async def _aio_get_result(self, url_postfix: str = EndpointPostfixEnm.GET_TASK_RESULT.value) -> CaptchaResponseSer:
        """
        Function send the ASYNC request to service and wait for result
        """
        # initial waiting
        await asyncio.sleep(self.__params.sleep_time)

        self.get_result_params.taskId = self.created_task_data.taskId
        attempts = attempts_generator()
        async with aiohttp.ClientSession() as session:
            for _ in attempts:
                try:
                    async with session.post(
                        parse.urljoin(self.__request_url, url_postfix), json=self.get_result_params.to_dict()
                    ) as resp:
                        if resp.status in VALID_STATUS_CODES:
                            result_data = CaptchaResponseSer(**await resp.json())
                            if result_data.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Failed):
                                # if captcha ready\failed or have unknown status - return exist data
                                return result_data
                        else:
                            raise ValueError(resp.reason)
                except Exception as error:
                    logging.exception(error)
                    raise

                # if captcha just created or in processing now - wait
                await asyncio.sleep(self.__params.sleep_time)

            # default response if server is silent
            return CaptchaResponseSer(
                errorId=1,
                errorCode="ERROR_CAPTCHA_UNSOLVABLE",
                errorDescription="Captcha not recognized",
                taskId=self.created_task_data.taskId,
                status=ResponseStatusEnm.Failed,
            )
