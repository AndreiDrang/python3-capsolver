from typing import Union

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("MtCaptcha",)


class MtCaptcha(CaptchaParams):
    """
    The class is used to work with Capsolver MtCaptcha captcha solving methods:
     - MtCaptchaTask
     - MtCaptchaTaskProxyLess

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``MtCaptchaTaskProxyLess`` and etc.
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used

    Examples:
        >>> from python3_capsolver.mt_captcha import MtCaptcha
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> MtCaptcha(api_key="CAI-12345....",
        ...             captcha_type=CaptchaTypeEnm.MtCaptchaTaskProxyLess)
        ...         .captcha_handler(task_payload={"websiteURL": "some-url"})
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
              "token": ""
           }
        }

        >>> import asyncio
        >>> from python3_capsolver.mt_captcha import MtCaptcha
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> asyncio.run(MtCaptcha(api_key="CAI-12345....",
        ...             captcha_type=CaptchaTypeEnm.MtCaptchaTaskProxyLess)
        ...         .aio_captcha_handler(task_payload={"websiteURL": "some-url"}))
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
              "token": ""
           }
        }

    Notes:
        https://docs.capsolver.com/en/guide/captcha/MtCaptcha/
    """

    def __init__(self, api_key: str, captcha_type: Union[CaptchaTypeEnm, str], **kwargs):

        super().__init__(api_key=api_key, captcha_type=captcha_type, **kwargs)
