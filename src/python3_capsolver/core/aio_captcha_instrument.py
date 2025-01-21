import asyncio
import logging
from typing import Optional
from urllib import parse

import aiohttp

from .enum import ResponseStatusEnm, EndpointPostfixEnm
from .const import REQUEST_URL, VALID_STATUS_CODES
from .utils import attempts_generator
from .serializer import CaptchaResponseSer
from .captcha_instrument import CaptchaInstrumentBase

__all__ = ("AIOCaptchaInstrument",)


class AIOCaptchaInstrument(CaptchaInstrumentBase):
    """
    Instrument for working with async captcha
    """

    def __init__(self, captcha_params: "CaptchaParams"):
        super().__init__()
        self.captcha_params = captcha_params
        self.created_task_data = CaptchaResponseSer

    async def processing_captcha(self) -> dict:
        self.captcha_params.create_task_payload.task = self.captcha_params.task_params
        self.created_task_data = CaptchaResponseSer(**await self.__create_task())

        # if task created and already ready - return result
        if self.created_task_data.errorId == 0 and self.created_task_data.status == ResponseStatusEnm.Processing.value:
            return (await self.__get_result()).to_dict()
        elif self.created_task_data.errorId != 0:
            self.created_task_data.status = ResponseStatusEnm.Failed

        return self.created_task_data.to_dict()

    async def __create_task(self, url_postfix: str = EndpointPostfixEnm.CREATE_TASK.value) -> dict:
        """
        Function send the ASYNC request to service and wait for result
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    parse.urljoin(self.captcha_params.request_url, url_postfix),
                    json=self.captcha_params.create_task_payload.to_dict(),
                ) as resp:
                    if resp.status in VALID_STATUS_CODES:
                        return await resp.json()
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise

    async def __get_result(self, url_postfix: str = EndpointPostfixEnm.GET_TASK_RESULT.value) -> CaptchaResponseSer:
        """
        Function send the ASYNC request to service and wait for result
        """
        # initial waiting
        await asyncio.sleep(self.captcha_params.sleep_time)

        self.captcha_params.get_result_params.taskId = self.created_task_data.taskId
        attempts = attempts_generator()
        async with aiohttp.ClientSession() as session:
            for _ in attempts:
                try:
                    async with session.post(
                        parse.urljoin(self.captcha_params.request_url, url_postfix),
                        json=self.captcha_params.get_result_params.to_dict(),
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
                await asyncio.sleep(self.captcha_params.sleep_time)

        # default response if server is silent
        self.result.errorId = 1
        self.result.errorCode = self.CAPTCHA_UNSOLVABLE
        self.result.errorDescription = self.CAPTCHA_UNSOLVABLE_DESCRIPTION
        self.result.taskId = self.created_task_data.taskId
        self.result.status = ResponseStatusEnm.Failed

    @staticmethod
    async def send_post_request(
        payload: Optional[dict] = None, url_postfix: EndpointPostfixEnm = EndpointPostfixEnm.GET_BALANCE
    ) -> dict:
        """
        Function send ASYNC request to service and wait for result
        """

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(parse.urljoin(REQUEST_URL, url_postfix.value), json=payload) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        raise ValueError(resp.status)
            except Exception as error:
                logging.exception(error)
                raise
