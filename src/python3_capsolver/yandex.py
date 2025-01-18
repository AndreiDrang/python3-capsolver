from typing import Union

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("YandexCaptcha",)


class YandexCaptcha(CaptchaParams):
    """
    The class is used to work with Capsolver YandexCaptchaTaskProxyLess methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``YandexCaptchaTaskProxyLess`` and etc.
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used

    Examples:
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> from python3_capsolver.yandex import YandexCaptcha
        >>> YandexCaptcha(api_key="CAP-XXXXX",
        ...         captcha_type=CaptchaTypeEnm.YandexCaptchaTaskProxyLess,
        ...         ).captcha_handler(task_payload={
        ...                                 "websiteURL": "https://www.yourwebsite.com",
        ...                                 "websiteKey": "ysc1_bFdbbET5WBnPTvoE5jTXxxxx"
        ...                         })
        {
            "errorId":0,
            "errorCode":"None",
            "errorDescription":"None",
            "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
            "status":"ready",
            "solution":{
                "token": "dD0xNzMzMjc0MjkzO2k9Nxxxx"
            }
        }

        >>> import asyncio
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> from python3_capsolver.yandex import YandexCaptcha
        >>> asyncio.run(YandexCaptcha(api_key="CAP-XXXXX",
        ...         captcha_type=CaptchaTypeEnm.YandexCaptchaTaskProxyLess,
        ...         ).aio_captcha_handler(task_payload={
        ...                                 "websiteURL": "https://www.yourwebsite.com",
        ...                                 "websiteKey": "ysc1_bFdbbET5WBnPTvoE5jTXxxxx"
        ...                         }))
        {
            "errorId":0,
            "errorCode":"None",
            "errorDescription":"None",
            "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
            "status":"ready",
            "solution":{
                "token": "dD0xNzMzMjc0MjkzO2k9Nxxxx"
            }
        }

    Notes:
        https://docs.capsolver.com/en/guide/captcha/YandexCaptcha/
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.YandexCaptchaTaskProxyLess,
        **kwargs,
    ):

        super().__init__(api_key=api_key, captcha_type=captcha_type, **kwargs)
