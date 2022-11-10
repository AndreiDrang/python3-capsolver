from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enum import CaptchaTypeEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import CaptchaResponseSer, RequestCreateTaskSer


class BaseImageToText(BaseCaptcha):
    """
    The class is used to work with CaptchaAI Image captcha solving methods.

    Args:
        api_key: CaptchaAI API key
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests

    Examples:
        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> ImageToText(api_key="CAI-12345....").captcha_handler(body=body)
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> with ImageToText(api_key="CAI-12345....") as image_to_text_inst:
        ...    image_to_text_inst.captcha_handler(body=body)
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> await ImageToText(api_key="CAI-12345....").aio_captcha_handler(body=body)
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> with ImageToText(api_key="CAI-12345....") as image_to_text_inst:
        ...    await image_to_text_inst.aio_captcha_handler(body=body)
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/393427
    """

    def __init__(
        self,
        api_key: str,
        sleep_time: int = 10,
        request_url: str = REQUEST_URL,
    ):

        super().__init__(
            api_key=api_key, sleep_time=sleep_time, request_url=request_url, captcha_type=CaptchaTypeEnm.ImageToTextTask
        )


class ImageToText(BaseImageToText):
    __doc__ = BaseImageToText.__doc__

    def captcha_handler(self, body: str, **additional_params) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            body: Base64 encoded content of the image
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key

        Examples:
            >>> with open('some_image.jpeg', 'rb') as img_file:
            ...    img_data = img_file.read()
            >>> body = base64.b64encode(img_data).decode("utf-8")
            >>> ImageToText(api_key="CAI-12345....").captcha_handler(body=body)
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'gRecaptchaResponse': '44795sds...'}
                              )

        Returns:
            CaptchaResponseSer model with full server response

        Notes:
            Check class docstirng for more info
        """
        return self._processing_captcha(
            serializer=RequestCreateTaskSer, type=self.captcha_type, body=body, **additional_params
        )

    async def aio_captcha_handler(self, body: str, **additional_params) -> CaptchaResponseSer:
        """
        Asynchronous method for captcha solving

        Args:
            body: Base64 encoded content of the image
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key

        Examples:
            >>> with open('some_image.jpeg', 'rb') as img_file:
            ...    img_data = img_file.read()
            >>> body = base64.b64encode(img_data).decode("utf-8")
            >>> await ImageToText(api_key="CAI-12345....").aio_captcha_handler(body=body)
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'gRecaptchaResponse': '44795sds...'}
                              )

        Returns:
            CaptchaResponseSer model with full server response

        Notes:
            Check class docstirng for more info
        """
        return await self._aio_processing_captcha(
            serializer=RequestCreateTaskSer, type=self.captcha_type, body=body, **additional_params
        )
