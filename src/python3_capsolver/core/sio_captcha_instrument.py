import time
import base64
import logging
from typing import Union, Optional
from urllib import parse

import requests
from requests.adapters import HTTPAdapter

from .enum import SaveFormatsEnm, ResponseStatusEnm, EndpointPostfixEnm
from .const import RETRIES, REQUEST_URL, VALID_STATUS_CODES, GET_BALANCE_POSTFIX
from .utils import attempts_generator
from .serializer import CaptchaResponseSer
from .captcha_instrument import CaptchaInstrument

__all__ = ("SIOCaptchaInstrument",)


class SIOCaptchaInstrument(CaptchaInstrument):
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
        self.created_task_data = CaptchaResponseSer(**self.__create_task())

        # if task created and ready - return result
        if self.created_task_data.errorId == 0 and self.created_task_data.status == ResponseStatusEnm.Processing:
            return self.__get_result().to_dict()
        return self.created_task_data.to_dict()

    def processing_image_captcha(
        self,
        save_format: Union[str, SaveFormatsEnm],
        img_clearing: bool,
        captcha_link: str,
        captcha_file: str,
        captcha_base64: bytes,
        img_path: str,
    ) -> dict:
        self.__body_file_processing(
            save_format=save_format,
            img_clearing=img_clearing,
            file_path=img_path,
            captcha_link=captcha_link,
            captcha_file=captcha_file,
            captcha_base64=captcha_base64,
        )
        if not self.result.errorId:
            return self.processing_captcha()
        return self.result.to_dict()

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
        self.result.errorDescription = "Captcha not recognized"
        self.result.taskId = self.created_task_data.taskId
        self.result.status = ResponseStatusEnm.Failed

    def __body_file_processing(
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
                content = self._url_read(url=captcha_link, **kwargs).content
                # according to the value of the passed parameter, select the function to save the image
                if save_format == SaveFormatsEnm.CONST.value:
                    full_file_path = self._file_const_saver(content, file_path, file_extension=file_extension)
                    if img_clearing:
                        self._file_clean(full_file_path=full_file_path)
                self.captcha_params.create_task_payload.task.update({"body": base64.b64encode(content).decode("utf-8")})
            except Exception as error:
                self.result.errorId = 1
                self.result.errorCode = self.CAPTCHA_UNSOLVABLE
                self.result.errorDescription = str(error)

        else:
            self.result.errorId = 1
            self.result.errorCode = self.CAPTCHA_UNSOLVABLE

    @staticmethod
    def send_post_request(
        payload: Optional[dict] = None,
        session: requests.Session = requests.Session(),
        url_postfix: str = GET_BALANCE_POSTFIX,
    ) -> dict:
        """
        Function send SYNC request to service and wait for result
        """
        try:
            resp = session.post(parse.urljoin(REQUEST_URL, url_postfix), json=payload)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise ValueError(resp.raise_for_status())
        except Exception as error:
            logging.exception(error)
            raise

    def _url_read(self, url: str, **kwargs):
        """
        Method open links
        """
        return self.session.get(url=url, **kwargs)
