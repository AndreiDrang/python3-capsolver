import logging
from typing import Any, Dict, Type
from urllib import parse

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from src.python3_captchaai.core.config import RETRIES, REQUEST_URL, VALID_STATUS_CODES
from src.python3_captchaai.core.serializer import PostRequestSer, CaptchaOptionsSer


class BaseCaptcha:
    def __init__(
        self,
        api_key: str,
        sleep_time: int = 10,
        request_url: str = REQUEST_URL,
        **kwargs,
    ):
        """
        Basic Captcha solving class

        Args:
            api_key: CaptchaAI API key
            sleep_time: The waiting time between requests to get the result of the Captcha
            request_url: API address for sending requests
            **kwargs:
        """
        # assign args to validator
        self.__params = CaptchaOptionsSer(**locals())
        self.__request_url = request_url

        # prepare session
        self.__session = requests.Session()
        self.__session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self.__session.mount("https://", HTTPAdapter(max_retries=RETRIES))

    def _prepare_create_task_payload(
        self, serializer: Type[PostRequestSer], create_params: Dict[str, Any] = None
    ) -> None:
        """
        Method prepare `createTask` payload

        Args:
            serializer: Serializer for task creation
            create_params: Parameters for task creation payload

        Examples:

            >>> self._prepare_create_task_payload(serializer=PostRequestSer, create_params={})

        """
        self.create_task_payload = serializer(clientKey=self.__params.api_key, **create_params if create_params else {})
        self.create_task_payload = self.create_task_payload.dict(by_alias=True)

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

    def _create_sync_task(self, url_postfix: str) -> dict:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = self.__session.post(parse.urljoin(self.__request_url, url_postfix), json=self.create_task_payload)
            if resp.status_code in VALID_STATUS_CODES:
                return resp.json()
            elif resp.status_code == 401:
                raise ValueError("Authentication failed, indicating that the API key is not correct")
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    def _get_sync_result(self, url_postfix: str) -> dict:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = self.__session.post(parse.urljoin(self.__request_url, url_postfix), json=self.__post_payload)
            if resp.status_code in VALID_STATUS_CODES:
                return resp.json()
            elif resp.status_code == 401:
                raise ValueError("Authentication failed, indicating that the API key is not correct")
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    async def _create_async_task(self, url_postfix: str) -> dict:
        """
        Function send the ASYNC request to service and wait for result
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    parse.urljoin(self.__request_url, url_postfix), json=self.create_task_payload
                ) as resp:
                    if resp.status in VALID_STATUS_CODES:
                        return await resp.json()
                    elif resp.status == 401:
                        raise ValueError("Authentication failed, indicating that the API key is not correct")
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise

    async def _get_async_result(self, url_postfix: str) -> dict:
        """
        Function send the ASYNC request to service and wait for result
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    parse.urljoin(self.__request_url, url_postfix), json=self.__post_payload
                ) as resp:
                    if resp.status in VALID_STATUS_CODES:
                        return await resp.json()
                    elif resp.status == 401:
                        raise ValueError("Authentication failed, indicating that the API key is not correct")
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise
