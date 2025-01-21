import time
import logging
from typing import Optional
from urllib import parse

import requests
from requests.adapters import HTTPAdapter

from .enum import ResponseStatusEnm, EndpointPostfixEnm
from .const import RETRIES, REQUEST_URL, VALID_STATUS_CODES
from .utils import attempts_generator
from .serializer import CaptchaResponseSer
from .captcha_instrument import CaptchaInstrumentBase

__all__ = ("SIOCaptchaInstrument",)


class SIOCaptchaInstrument(CaptchaInstrumentBase):
    """
    Instrument for working with sync captcha
    """

    def __init__(self, captcha_params: "CaptchaParams"):
        super().__init__()
        self.captcha_params = captcha_params
        self.created_task_data = CaptchaResponseSer
        # prepare session
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        self.session.mount("https://", HTTPAdapter(max_retries=RETRIES))
        self.session.verify = False

    def processing_captcha(self) -> dict:
        self.captcha_params.create_task_payload.task = self.captcha_params.task_params

        self.created_task_data = CaptchaResponseSer(**self.__create_task())

        # if task created and ready - return result
        if self.created_task_data.errorId == 0 and self.created_task_data.status == ResponseStatusEnm.Processing:
            return self.__get_result().to_dict()
        elif self.created_task_data.errorId != 0:
            self.created_task_data.status = ResponseStatusEnm.Failed

        return self.created_task_data.to_dict()

    def __create_task(self, url_postfix: str = EndpointPostfixEnm.CREATE_TASK.value) -> dict:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = self.session.post(
                parse.urljoin(self.captcha_params.request_url, url_postfix),
                json=self.captcha_params.create_task_payload.to_dict(),
            )
            if resp.status_code in VALID_STATUS_CODES:
                return resp.json()
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    def __get_result(self, url_postfix: str = EndpointPostfixEnm.GET_TASK_RESULT.value) -> CaptchaResponseSer:
        """
        Method send SYNC request to service and wait for result
        """
        # initial waiting
        time.sleep(self.captcha_params.sleep_time)

        self.captcha_params.get_result_params.taskId = self.created_task_data.taskId

        attempts = attempts_generator()
        for _ in attempts:
            try:
                resp = self.session.post(
                    parse.urljoin(self.captcha_params.request_url, url_postfix),
                    json=self.captcha_params.get_result_params.to_dict(),
                )
                if resp.status_code in VALID_STATUS_CODES:
                    result_data = CaptchaResponseSer(**resp.json())
                    if result_data.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Failed):
                        # if captcha ready\failed or have unknown status - return exist data
                        return result_data
                else:
                    raise ValueError(resp.raise_for_status())
            except Exception as error:
                logging.exception(error)
                raise

            # if captcha just created or in processing now - wait
            time.sleep(self.captcha_params.sleep_time)
        # default response if server is silent
        self.result.errorId = 1
        self.result.errorCode = self.CAPTCHA_UNSOLVABLE
        self.result.errorDescription = self.CAPTCHA_UNSOLVABLE_DESCRIPTION
        self.result.taskId = self.created_task_data.taskId
        self.result.status = ResponseStatusEnm.Failed

    @staticmethod
    def send_post_request(
        payload: Optional[dict] = None,
        session: requests.Session = requests.Session(),
        url_postfix: EndpointPostfixEnm = EndpointPostfixEnm.GET_BALANCE,
    ) -> dict:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = session.post(parse.urljoin(REQUEST_URL, url_postfix.value), json=payload)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise ValueError(resp.status_code)
        except Exception as error:
            logging.exception(error)
            raise
