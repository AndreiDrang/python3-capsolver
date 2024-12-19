import base64
import asyncio
import logging
from typing import Union, Optional
from urllib import parse

import aiohttp

from .enum import SaveFormatsEnm, ResponseStatusEnm, EndpointPostfixEnm
from .const import REQUEST_URL, ASYNC_RETRIES, VALID_STATUS_CODES, GET_BALANCE_POSTFIX
from .utils import attempts_generator
from .serializer import CaptchaResponseSer
from .captcha_instrument import CaptchaInstrument

__all__ = ("AIOCaptchaInstrument",)


class AIOCaptchaInstrument(CaptchaInstrument):
    """
    Instrument for working with async captcha
    """

    def __init__(self, captcha_params: "CaptchaParams"):
        super().__init__()
        self.captcha_params = captcha_params
        self.created_task_data = CaptchaResponseSer

    async def processing_captcha(self) -> dict:
        self.created_task_data = CaptchaResponseSer(**await self.__create_task())

        # if task created and already ready - return result
        if self.created_task_data.errorId == 0 and self.created_task_data.status == ResponseStatusEnm.Processing.value:
            return (await self.__get_result()).to_dict()
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
            self.result.errorDescription = "Captcha not recognized"
            self.result.taskId = self.created_task_data.taskId
            self.result.status = ResponseStatusEnm.Failed

    async def processing_image_captcha(
        self,
        save_format: Union[str, SaveFormatsEnm],
        img_clearing: bool,
        captcha_link: str,
        captcha_file: str,
        captcha_base64: bytes,
        img_path: str,
    ) -> dict:
        await self.__body_file_processing(
            save_format=save_format,
            img_clearing=img_clearing,
            file_path=img_path,
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
        )
        if not self.result.errorId:
            return await self.processing_captcha()
        return self.result.to_dict()

    async def __body_file_processing(
        self,
        save_format: SaveFormatsEnm,
        img_clearing: bool,
        file_path: str,
        file_extension: str = "png",
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        **kwargs,
    ):
        # if a local file link is passed
        if captcha_file:
            self.captcha_params.create_task_payload.task.update(
                {"body": base64.b64encode(self._local_file_captcha(captcha_file=captcha_file)).decode("utf-8")}
            )
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            self.captcha_params.create_task_payload.task.update(
                {"body": base64.b64encode(captcha_base64).decode("utf-8")}
            )
        # if a URL is passed
        elif captcha_link:
            try:
                content = await self._url_read(url=captcha_link, **kwargs)
                # according to the value of the passed parameter, select the function to save the image
                if save_format == SaveFormatsEnm.CONST.value:
                    full_file_path = self._file_const_saver(content, file_path, file_extension=file_extension)
                    if img_clearing:
                        self._file_clean(full_file_path=full_file_path)
                self.captcha_params.create_task_payload.task.update({"body": base64.b64encode(content).decode("utf-8")})
            except Exception as error:
                self.result.errorId = 12
                self.result.errorCode = self.CAPTCHA_UNSOLVABLE
                self.result.errorDescription = str(error)

        else:
            self.result.errorId = 12
            self.result.errorCode = self.CAPTCHA_UNSOLVABLE

    @staticmethod
    async def send_post_request(payload: Optional[dict] = None, url_postfix: str = GET_BALANCE_POSTFIX) -> dict:
        """
        Function send ASYNC request to service and wait for result
        """

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(parse.urljoin(REQUEST_URL, url_postfix), json=payload) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise

    @staticmethod
    async def _url_read(url: str, **kwargs) -> bytes:
        """
        Async method read bytes from link
        """
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.get(url=url, **kwargs) as resp:
                        return await resp.content.read()
