from typing import Union

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("Cloudflare",)


class Cloudflare(CaptchaParams):
    """
    The class is used to work with Capsolver AntiTurnstileTaskProxyLess captcha solving method

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``AntiTurnstileTaskProxyLess`` and etc.
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used

    Examples:
        >>> from python3_capsolver.cloudflare import Cloudflare
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> Cloudflare(api_key="CAI-12345....",
        ...             captcha_type=CaptchaTypeEnm.AntiTurnstileTaskProxyLess)
        ...         .captcha_handler(task_payload={
        ...                     "websiteKey": "0x4XXXXXXXXXXXXXXXXX",
        ...                     "metadata": {
        ...                         "action": "login",
        ...                         "cdata": "0000-1111-2222-3333-example-cdata"
        ...                     }
        ...         })
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
                "token": "0.mF74FV8wEufAWxxxx",
                "type": "turnstile",
                "userAgent": "Mozilla/5.0 xxxx"
           }
        }

    Notes:
        https://docs.capsolver.com/en/guide/captcha/cloudflare_turnstile/
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.AntiTurnstileTaskProxyLess,
        **kwargs,
    ):

        super().__init__(api_key=api_key, captcha_type=captcha_type, **kwargs)
