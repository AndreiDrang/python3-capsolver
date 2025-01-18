from typing import Any, Dict

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("VisionEngine",)


class VisionEngine(CaptchaParams):
    """
    The class is used to work with Capsolver VisionEngine captcha solving method.

    Args:
        api_key: Capsolver API key
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used

    Examples:
        >>> from python3_capsolver.vision_engine import VisionEngine
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> VisionEngine(api_key="CAI-12345....").captcha_handler(
        ...                             task_payload={
        ...                                 "image": body,
        ...                                 "question": "click on the unique object",
        ...                                 "module": "space_detection",
        ...                             }
        ...                     )
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
              "box": [163.5, 107.5]
           }
        }

        >>> import asyncio
        >>> from python3_capsolver.vision_engine import VisionEngine
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> asyncio.run(VisionEngine(api_key="CAI-12345....").aio_captcha_handler(
        ...                             task_payload={
        ...                                 "image": body,
        ...                                 "question": "click on the unique object",
        ...                                 "module": "space_detection",
        ...                             }
        ...                     ))
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
              "box": [163.5, 107.5]
           }
        }

    Notes:
        https://docs.capsolver.com/en/guide/recognition/VisionEngine/
    """

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key=api_key, captcha_type=CaptchaTypeEnm.VisionEngine, **kwargs)

    def captcha_handler(self, task_payload: Dict) -> Dict[str, Any]:
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
        return super().captcha_handler(task_payload=task_payload)

    async def aio_captcha_handler(self, task_payload: Dict) -> Dict[str, Any]:
        """
        Asynchronous method for captcha solving

        Args:
            task_payload: Captcha solving `task` payload, include `question`, `image` and other fields.

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        task_payload.pop("type", None)
        return await super().aio_captcha_handler(task_payload=task_payload)
