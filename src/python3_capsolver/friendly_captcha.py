from typing import Union

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("FriendlyCaptcha",)


class FriendlyCaptcha(CaptchaParams):
    """
    The class is used to work with Capsolver FriendlyCaptchaTaskProxyless methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``FriendlyCaptchaTaskProxyless`` and etc.
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used

    Examples:
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> from python3_capsolver.friendly_captcha import FriendlyCaptcha
        >>> FriendlyCaptcha(api_key="CAP-XXXXX",
        ...         captcha_type=CaptchaTypeEnm.FriendlyCaptchaTaskProxyless,
        ...         ).captcha_handler(task_payload={
        ...                                 "websiteURL": "https://www.yourwebsite.com",
        ...                                 "proxy": "ip:port:user:pass"
        ...                         })
        {
            "errorId":0,
            "errorCode":"None",
            "errorDescription":"None",
            "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
            "status":"ready",
            "solution":{
                "cookies": "cf_clearance=_VPxxxx",
                "headers": {
                    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "accept": "text/html,axxxx",
                    "User-Agent": "Mozilla/5.0xxxx",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-user": "?1",
                    "referer": "https://www.yourwebsite.com",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "accept-language": "en",
                },
                "page_url": "https://www.yourwebsite.com",
                "proxy": "your proxyxxxx",
                "token": "_VPCTZXP5bhinxxxx"
            }
        }

    Notes:
        https://docs.capsolver.com/en/guide/captcha/FriendlyCaptcha/
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.FriendlyCaptchaTaskProxyless,
        **kwargs,
    ):

        super().__init__(api_key=api_key, captcha_type=captcha_type, **kwargs)
