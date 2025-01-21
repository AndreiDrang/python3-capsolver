from typing import Union

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("ImageToText",)


class ImageToText(CaptchaParams):
    """
    The class is used to work with Capsolver Image captcha solving method.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``ImageToTextTask`` and etc.
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used

    Examples:
        >>> from python3_capsolver.image_to_text import ImageToText
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> ImageToText(api_key="CAI-12345....").captcha_handler(
        ...                     task_payload={"body": body, "module": "common"}
        ...                    )
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
              "confidence":0.9585,
              "text":"gcphjd"
           }
        }

        >>> import asyncio
        >>> from python3_capsolver.image_to_text import ImageToText
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> asyncio.run(ImageToText(api_key="CAI-12345....").aio_captcha_handler(
        ...                     task_payload={"body": body, "module": "common"}
        ...                     )
        ...         )
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
              "confidence":0.9585,
              "text":"gcphjd"
           }
        }

        >>> from python3_capsolver.image_to_text import ImageToText
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> ImageToText(api_key="CAI-12345....").captcha_handler(
        ...                     task_payload={"body": body,
        ...                                     "module": "common",
        ...                                     "score": 0.92}
        ...                     )
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
              "confidence":0.9585,
              "text":"gcphjd"
           }
        }

    Notes:
        https://docs.capsolver.com/guide/recognition/ImageToTextTask.html
    """

    def __init__(
        self, api_key: str, captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.ImageToTextTask, **kwargs
    ):

        super().__init__(api_key=api_key, captcha_type=captcha_type, **kwargs)
