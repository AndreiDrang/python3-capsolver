import time
import asyncio
import logging
from urllib import parse

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from python3_captchaai.core.config import RETRIES, REQUEST_URL, ASYNC_RETRIES, VALID_STATUS_CODES
from python3_captchaai.core.serializer import ResponseSer, PostRequestSer, CaptchaOptionsSer


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

        # prepare POST payload
        self.__post_payload = PostRequestSer(clientKey=self.__params.api_key).dict(by_alias=True)
        # prepare result payload
        self.__result = ResponseSer()

        # If more parameters are passed, add them to post_payload
        if kwargs:
            for key in kwargs:
                self.__post_payload.update({key: kwargs[key]})

        # prepare session
        self.__session = requests.Session()
        self.__session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self.__session.mount("https://", HTTPAdapter(max_retries=RETRIES))

    def _processing_response(self, **kwargs: dict) -> dict:
        """
        Method processing captcha solving task creation result
        :param kwargs: additional params for Requests library
        """
        try:
            response = ResponseSer(
                **self.__session.post(self.__params.url_request, data=self.__post_payload, **kwargs).json()
            )
            # check response status
            if response.status == 1:
                self.__result.taskId = response.request
            else:
                self.__result.error = True
                self.__result.errorBody = response.request
        except Exception as error:
            self.__result.error = True
            self.__result.errorBody = error

        # check for errors while make request to server
        if self.__result.error:
            return self.__result.dict(exclude_none=True)

        # if all is ok - send captcha to service and wait solution
        # update payload - add captcha taskId
        self.__get_payload.update({"id": self.__result.taskId})

        # wait captcha solving
        time.sleep(self.__params.sleep_time)
        return self._get_sync_result(
            get_payload=self.__get_payload,
            sleep_time=self.__params.sleep_time,
            url_response=self.__params.url_response,
            result=self.__result,
        )

    def _url_open(self, url: str, **kwargs):
        """
        Method open links
        """
        return self.__session.get(url=url, **kwargs)

    async def _aio_url_read(self, url: str, **kwargs) -> bytes:
        """
        Async method read bytes from link
        """
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.get(url=url, **kwargs) as resp:
                        return await resp.content.read()

    async def _aio_processing_response(self) -> dict:
        """
        Method processing async captcha solving task creation result
        """
        try:
            # make async or sync request
            response = await self.__aio_make_post_request()
            # check response status
            if response.status == 1:
                self.__result.taskId = response.request
            else:
                self.__result.error = True
                self.__result.errorBody = response.request
        except Exception as error:
            self.__result.error = True
            self.__result.errorBody = error

        # check for errors while make request to server
        if self.__result.error:
            return self.__result.dict(exclude_none=True)

        # if all is ok - send captcha to service and wait solution
        # update payload - add captcha taskId
        self.__get_payload.update({"id": self.__result.taskId})

        # wait captcha solving
        await asyncio.sleep(self.__params.sleep_time)
        return await self._get_async_result(
            get_payload=self.__get_payload,
            sleep_time=self.__params.sleep_time,
            url_response=self.__request_url,
            result=self.__result,
        )

    async def __aio_make_post_request(self) -> ResponseSer:
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.post(
                        self.__request_url, data=self.__post_payload, raise_for_status=True
                    ) as resp:
                        response_json = await resp.json()
                        return ResponseSer(**response_json)

    def _result_processing(self, captcha_response: ResponseSer, result: ResponseSer) -> dict:
        """
        Function processing service response status values
        """

        # on error during solving
        if captcha_response.status == 0:
            result.error = True
            result.errorBody = captcha_response.request

        # if solving is success
        elif captcha_response.status == 1:
            result.captchaSolve = captcha_response.request

            # if this is ReCaptcha v3 then we get it from the server
            if captcha_response.user_check and captcha_response.user_score:
                result = result.dict()
                result.update(
                    {
                        "user_check": captcha_response.user_check,
                        "user_score": captcha_response.user_score,
                    }
                )
                return result

        return result.dict()

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

    def _get_sync_result(self, url_postfix: str) -> ResponseSer:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = self.__session.post(parse.urljoin(self.__request_url, url_postfix), json=self.__post_payload)
            if resp.status_code in VALID_STATUS_CODES:
                return ResponseSer(**resp.json())
            elif resp.status_code == 401:
                raise ValueError("Authentication failed, indicating that the API key is not correct")
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    async def _get_async_result(self, url_postfix: str) -> ResponseSer:
        """
        Function send the ASYNC request to service and wait for result
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    parse.urljoin(self.__request_url, url_postfix), json=self.__post_payload
                ) as resp:
                    if resp.status in VALID_STATUS_CODES:
                        resp_json = await resp.json()
                        return ResponseSer(**resp_json)
                    elif resp.status == 401:
                        raise ValueError("Authentication failed, indicating that the API key is not correct")
                    else:
                        raise ValueError(resp.reason)
            except Exception as error:
                logging.exception(error)
                raise
