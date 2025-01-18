from typing import Union

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm


class DatadomeSlider(CaptchaParams):
    """
    The class is used to work with Capsolver DatadomeSliderTask method.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``DatadomeSliderTask`` and etc.
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used

    Examples:
        >>> from python3_capsolver.datadome_slider import DatadomeSlider
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> DatadomeSlider(api_key="CAI-12345....",
        ...             captcha_type=CaptchaTypeEnm.DatadomeSliderTask)
        ...         .captcha_handler(task_payload={
        ...                 "captchaUrl": "https://geo.captchaxxxxxx",
        ...                 "userAgent": "Mozilla/5.0 xxxx",
        ...                 "proxy": "0.0.0.0:334:user:pass"
        ...         })
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
                "userAgent": "Mozilla/5.0 xxxx",
                "cookie": "datadome=yzj_BK..xxxx"
           }
        }

        >>> import asyncio
        >>> from python3_capsolver.datadome_slider import DatadomeSlider
        >>> from python3_capsolver.core.enum import CaptchaTypeEnm
        >>> asyncio.run(DatadomeSlider(api_key="CAI-12345....",
        ...             captcha_type=CaptchaTypeEnm.DatadomeSliderTask)
        ...         .aio_captcha_handler(task_payload={
        ...                 "captchaUrl": "https://geo.captchaxxxxxx",
        ...                 "userAgent": "Mozilla/5.0 xxxx",
        ...                 "proxy": "0.0.0.0:334:user:pass"
        ...         }))
        {
           "errorId":0,
           "errorCode":"None",
           "errorDescription":"None",
           "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
           "status":"ready",
           "solution":{
                "userAgent": "Mozilla/5.0 xxxx",
                "cookie": "datadome=yzj_BK..xxxx"
           }
        }

    Notes:
        https://docs.capsolver.com/en/guide/captcha/datadome/
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.DatadomeSliderTask,
        **kwargs,
    ):

        super().__init__(api_key=api_key, captcha_type=captcha_type, **kwargs)
