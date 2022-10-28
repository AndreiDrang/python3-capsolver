import time
import asyncio

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from .config import RETRIES, REQUEST_URL, ASYNC_RETRIES, connect_generator
from .serializer import (
    ResponseSer,
    GetRequestSer,
    PostRequestSer,
    CaptchaOptionsSer,
    ServiceGetResponseSer,
    ServicePostResponseSer,
)


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

        # prepare POST payload
        self.__post_payload = PostRequestSer(key=self.__params.api_key).dict(by_alias=True)
        # prepare GET payload
        self.__get_payload = GetRequestSer(key=self.__params.api_key).dict(
            by_alias=True, exclude_none=True
        )
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
            response = ServicePostResponseSer(
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
            url_response=self.__params.url_response,
            result=self.__result,
        )

    async def __aio_make_post_request(self) -> ServicePostResponseSer:
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.post(
                        self.__params.url_request, data=self.__post_payload, raise_for_status=True
                    ) as resp:
                        response_json = await resp.json()
                        return ServicePostResponseSer(**response_json)

    def _result_processing(self, captcha_response: ServiceGetResponseSer, result: ResponseSer) -> dict:
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

    def _get_sync_result(self, get_payload: dict, sleep_time: int, url_response: str, result: ResponseSer) -> dict:
        """
        Function periodically send the SYNC request to service and wait for captcha solving result
        """
        # generator for repeated attempts to connect to the server
        connect_gen = connect_generator()
        while True:
            try:
                # send a request for the result of solving the captcha
                captcha_response = ServiceGetResponseSer(**requests.get(url_response, params=get_payload).json())
                # if the captcha has not been resolved yet, wait
                if captcha_response.request == "CAPCHA_NOT_READY":
                    time.sleep(sleep_time)
                else:
                    return self._result_processing(captcha_response, result)

            except Exception as error:
                if next(connect_gen) < 4:
                    time.sleep(2)
                else:
                    result.error = True
                    result.errorBody = error
                    return result.dict()

    async def _get_async_result(
        self, get_payload: dict, sleep_time: int, url_response: str, result: ResponseSer
    ) -> dict:
        """
        Function periodically send the ASYNC request to service and wait for captcha solving result
        """
        # generator for repeated attempts to connect to the server
        connect_gen = connect_generator()
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    # send a request for the result of solving the captcha
                    async with session.get(url_response, params=get_payload, raise_for_status=True) as resp:
                        captcha_response = await resp.json()
                        captcha_response = ServiceGetResponseSer(**captcha_response)

                        # if the captcha has not been resolved yet, wait
                        if captcha_response.request == "CAPCHA_NOT_READY":
                            await asyncio.sleep(sleep_time)

                        else:
                            return self._result_processing(captcha_response, result)

                except Exception as error:
                    if next(connect_gen) < 4:
                        await asyncio.sleep(2)
                    else:
                        result.error = True
                        result.errorBody = error
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
