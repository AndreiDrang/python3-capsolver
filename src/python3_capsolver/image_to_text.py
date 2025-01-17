from typing import Dict

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm
from .core.aio_captcha_instrument import AIOCaptchaInstrument
from .core.sio_captcha_instrument import SIOCaptchaInstrument


class ImageToText(CaptchaParams):
    """
    The class is used to work with Capsolver Image captcha solving methods.

    Args:
        api_key: Capsolver API key

    Examples:
        >>> from python3_capsolver.image_to_text import ImageToText
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument

        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> ImageToText(api_key="CAI-12345....")captcha_handler(
        >>>                     task_payload={"body": body, "module": "common"}
        >>>                     )
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
        >>>                     task_payload={"body": body, "module": "common"}
        >>>                     )
        >>>         )
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
        >>> ImageToText(api_key="CAI-12345....")captcha_handler(
        >>>                     task_payload={"body": body,
        >>>                                     "module": "common",
        >>>                                     "score": 0.92}
        >>>                     )
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

    Returns:
        Dict with full server response

    Notes:
        https://docs.capsolver.com/guide/recognition/ImageToTextTask.html
    """

    def __init__(self, api_key: str, **kwargs):

        super().__init__(api_key=api_key, captcha_type=CaptchaTypeEnm.ImageToTextTask, **kwargs)

    def captcha_handler(self, task_payload: Dict) -> Dict[str, str]:
        """
        Synchronous method for captcha solving

        Args:
            task_payload: Captcha solving `task` payload, include `body`, `module` and other fields.

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        task_payload.pop("type", None)
        self.task_params.update(task_payload)
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.processing_captcha()

    async def aio_captcha_handler(self, task_payload: Dict) -> Dict[str, str]:
        """
        Asynchronous method for captcha solving

        Args:
            task_payload: Captcha solving `task` payload, include `body`, `module` and other fields.

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        task_payload.pop("type", None)
        self.task_params.update(task_payload)
        self._captcha_handling_instrument = AIOCaptchaInstrument(captcha_params=self)
        return await self._captcha_handling_instrument.processing_captcha()
