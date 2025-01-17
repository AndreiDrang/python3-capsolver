from typing import Dict

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("ReCaptchaV2Classification",)


class ReCaptchaV2Classification(CaptchaParams):
    """
    The class is used to work with Capsolver ReCaptchaV2Classification captcha solving method.

    Args:
        api_key: Capsolver API key

    Examples:
        >>> from python3_capsolver.recaptchav2_classification import ReCaptchaV2Classification
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument

        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> ReCaptchaV2Classification(api_key="CAI-12345....").captcha_handler(
        >>>                             task_payload={"image": body, "question": "/m/04_sv"}
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
        >>> from python3_capsolver.recaptchav2_classification import ReCaptchaV2Classification
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument

        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> asyncio.run(ReCaptchaV2Classification(api_key="CAI-12345....").aio_captcha_handler(
        >>>                                         task_payload={"image": body, "question": "/m/04_sv"}
        >>>                                 )
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

        >>> from python3_capsolver.recaptchav2_classification import ReCaptchaV2Classification
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument

        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> ReCaptchaV2Classification(api_key="CAI-12345....").captcha_handler(
        >>>                             task_payload={"image": body, "question": "/m/04_sv"}
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
        https://docs.capsolver.com/en/guide/recognition/ReCaptchaClassification/
    """

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key=api_key, captcha_type=CaptchaTypeEnm.ReCaptchaV2Classification, **kwargs)

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
        return super().captcha_handler(task_payload=task_payload)

    async def aio_captcha_handler(self, task_payload: Dict) -> Dict[str, str]:
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
