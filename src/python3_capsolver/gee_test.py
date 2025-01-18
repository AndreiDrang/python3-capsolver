from typing import Union

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("GeeTest",)


class GeeTest(CaptchaParams):
    """
    The class is used to work with Capsolver GeeTestTaskProxyLess methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``GeeTestTaskProxyLess`` and etc.
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used

    Examples:
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> from python3_capsolver.gee_test import GeeTest

        >>> GeeTest(api_key="CAP-XXXXX",
        ...         captcha_type=CaptchaTypeEnm.GeeTestTaskProxyLess,
        ...         ).captcha_handler(task_payload={
        ...                                 "websiteURL": "https://www.geetest.com/en/demo",
        ...                                 "gt": "022397c99c9f646f6477822485f30404",
        ...                                 "challenge": "12345678abc90123d45678ef90123a456b",
        ...                         })
        {
            "errorId":0,
            "errorCode":"None",
            "errorDescription":"None",
            "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
            "status":"ready",
            "solution":{
                "challenge": "xxx",
                "validate": "xxx"
            }
        }

        >>> import asyncio
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> from python3_capsolver.gee_test import GeeTest

        >>> asyncio.run(GeeTest(api_key="CAP-XXXXX",
        ...         captcha_type=CaptchaTypeEnm.GeeTestTaskProxyLess,
        ...         ).aio_captcha_handler(task_payload={
        ...                                 "websiteURL": "https://www.geetest.com/en/demo",
        ...                                 "gt": "022397c99c9f646f6477822485f30404",
        ...                                 "challenge": "12345678abc90123d45678ef90123a456b",
        ...                         }))
        {
            "errorId":0,
            "errorCode":"None",
            "errorDescription":"None",
            "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
            "status":"ready",
            "solution":{
                "challenge": "xxx",
                "validate": "xxx"
            }
        }

    Notes:
        https://docs.capsolver.com/en/guide/captcha/Geetest/
    """

    def __init__(
        self, api_key: str, captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.GeeTestTaskProxyLess, **kwargs
    ):

        super().__init__(api_key=api_key, captcha_type=captcha_type, **kwargs)
