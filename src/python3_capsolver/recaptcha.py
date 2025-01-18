from typing import Union

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("ReCaptcha",)


class ReCaptcha(CaptchaParams):
    """
    The class is used to work with Capsolver ReCaptcha captcha solving methods:
     - ReCaptchaV2Classification
     - ReCaptchaV2Task
     - ReCaptchaV2EnterpriseTask
     - ReCaptchaV2TaskProxyLess
     - ReCaptchaV2EnterpriseTaskProxyLess
     - ReCaptchaV3Task
     - ReCaptchaV3EnterpriseTask
     - ReCaptchaV3TaskProxyLess
     - ReCaptchaV3EnterpriseTaskProxyLess

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``ReCaptchaV2Task`` and etc.
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used

    Examples:
        >>> from python3_capsolver.recaptcha import ReCaptcha
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> ReCaptcha(api_key="CAI-12345....",
        ...             captcha_type=CaptchaTypeEnm.ReCaptchaV2Classification)
        ...         .captcha_handler(task_payload={"image": body, "question": "/m/04_sv"})
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
        >>> from python3_capsolver.recaptcha import ReCaptcha
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        >>> asyncio.run(ReCaptcha(api_key="CAI-12345....").aio_captcha_handler(
        ...                                         task_payload={"image": body, "question": "/m/04_sv"}
        ...                                 )
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

    Notes:
        https://docs.capsolver.com/en/guide/recognition/ReCaptchaClassification/

        https://docs.capsolver.com/en/guide/captcha/ReCaptchaV2/

        https://docs.capsolver.com/en/guide/captcha/ReCaptchaV3/
    """

    def __init__(self, api_key: str, captcha_type: Union[CaptchaTypeEnm, str], **kwargs):

        super().__init__(api_key=api_key, captcha_type=captcha_type, **kwargs)
