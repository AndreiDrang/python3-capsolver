import time
import asyncio
import logging
from typing import Any, Dict, Type, Union
from urllib import parse

import aiohttp
import requests
from pydantic import BaseModel
from requests.adapters import HTTPAdapter

from python3_captchaai.core.enums import CaptchaTypeEnm, ResponseStatusEnm, EndpointPostfixEnm
from python3_captchaai.core.config import RETRIES, REQUEST_URL, VALID_STATUS_CODES, attempts_generator
from python3_captchaai.core.serializer import CaptchaOptionsSer, CaptchaResponseSer, RequestGetTaskResultSer


class BaseCaptcha:
    """
    Basic Captcha solving class

    Args:
        api_key: CaptchaAI API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        sleep_time: int = 10,
        request_url: str = REQUEST_URL,
    ):
        # validate captcha_type parameter
        if captcha_type in CaptchaTypeEnm.list_values():
            self.captcha_type = captcha_type
        else:
            raise ValueError(f"Invalid `captcha_type` parameter set, available - {CaptchaTypeEnm.list_values()}")

        # assign args to validator
        self.__params = CaptchaOptionsSer(**locals())
        self.__request_url = request_url

        # prepare session
        self.__session = requests.Session()
        self.__session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self.__session.mount("https://", HTTPAdapter(max_retries=RETRIES))

    def _prepare_create_task_payload(self, serializer: Type[BaseModel], create_params: Dict[str, Any] = None) -> None:
        """
        Method prepare `createTask` payload

        Args:
            serializer: Serializer for task creation
            create_params: Parameters for task creation payload

        Examples:

            >>> self._prepare_create_task_payload(serializer=PostRequestSer, create_params={})

        """
        self.task_payload = serializer(clientKey=self.__params.api_key)
        self.task_payload: Dict = self.task_payload.dict()
        # added task params to payload
        self.task_payload["task"] = {**create_params} if create_params else {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        return True

    """
    Sync part
    """

    def _processing_captcha(self, serializer: Type[BaseModel], **create_params) -> CaptchaResponseSer:
        self._prepare_create_task_payload(serializer=serializer, create_params=create_params)
        self.created_task_data = CaptchaResponseSer(**self._create_task())

        # if task created and already ready - return result
        if self.created_task_data.status == ResponseStatusEnm.Ready.value:
            return self.created_task_data
        # if captcha is not ready but task success created - waiting captcha result
        elif not self.created_task_data.errorId:
            return self._get_result()
        return self.created_task_data

    def _create_task(self, url_postfix: str = EndpointPostfixEnm.CREATE_TASK.value) -> dict:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = self.__session.post(parse.urljoin(self.__request_url, url_postfix), json=self.task_payload)
            if resp.status_code in VALID_STATUS_CODES:
                return resp.json()
            elif resp.status_code == 401:
                raise ValueError("Authentication failed, indicating that the API key is not correct")
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    def _get_result(self, url_postfix: str = EndpointPostfixEnm.GET_TASK_RESULT.value) -> CaptchaResponseSer:
        """
        Function send SYNC request to service and wait for result
        """
        get_result_payload = RequestGetTaskResultSer(
            clientKey=self.__params.api_key, taskId=self.created_task_data.taskId
        )
        attempts = attempts_generator()
        for attempt in attempts:
            try:
                resp = self.__session.post(
                    parse.urljoin(self.__request_url, url_postfix), json=get_result_payload.dict()
                )
                if resp.status_code in VALID_STATUS_CODES:
                    result_data = CaptchaResponseSer(**resp.json())
                    if result_data.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Failed):
                        # if captcha ready\failed or have unknown status - return exist data
                        return result_data
                elif resp.status_code == 401:
                    raise ValueError("Authentication failed, indicating that the API key is not correct")
                else:
                    raise ValueError(resp.raise_for_status())
            except Exception as error:
                logging.exception(error)
                raise

            # if captcha just created or in processing now - wait
            time.sleep(self.__params.sleep_time)

    """
    Async part
    """

    async def _aio_processing_captcha(self, serializer: Type[BaseModel], **create_params) -> CaptchaResponseSer:
        self._prepare_create_task_payload(serializer=serializer, create_params=create_params)
        self.created_task_data = CaptchaResponseSer(**await self._aio_create_task())

        # if task created and already ready - return result
        if self.created_task_data.status == ResponseStatusEnm.Ready.value:
            return self.created_task_data
        # if captcha is not ready but task success created - waiting captcha result
        elif not self.created_task_data.errorId:
            return await self._aio_get_result()
        return self.created_task_data

    async def _aio_create_task(self, url_postfix: str = EndpointPostfixEnm.CREATE_TASK.value) -> dict:
        """
        Function send the ASYNC request to service and wait for result
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(parse.urljoin(self.__request_url, url_postfix), json=self.task_payload) as resp:
                    if resp.status in VALID_STATUS_CODES:
                        return await resp.json()
                    elif resp.status == 401:
                        raise ValueError("Authentication failed, indicating that the API key is not correct")
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise

    async def _aio_get_result(self, url_postfix: str = EndpointPostfixEnm.GET_TASK_RESULT.value) -> CaptchaResponseSer:
        """
        Function send the ASYNC request to service and wait for result
        """
        get_result_payload = RequestGetTaskResultSer(
            clientKey=self.__params.api_key, taskId=self.created_task_data.taskId
        )
        attempts = attempts_generator()
        async with aiohttp.ClientSession() as session:
            for attempt in attempts:
                try:
                    async with session.post(
                        parse.urljoin(self.__request_url, url_postfix), json=get_result_payload.dict()
                    ) as resp:
                        if resp.status in VALID_STATUS_CODES:
                            result_data = CaptchaResponseSer(**await resp.json())
                            if result_data.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Failed):
                                # if captcha ready\failed or have unknown status - return exist data
                                return result_data
                        elif resp.status == 401:
                            raise ValueError("Authentication failed, indicating that the API key is not correct")
                        else:
                            raise ValueError(resp.reason)
                except Exception as error:
                    logging.exception(error)
                    raise

                # if captcha just created or in processing now - wait
                await asyncio.sleep(self.__params.sleep_time)
