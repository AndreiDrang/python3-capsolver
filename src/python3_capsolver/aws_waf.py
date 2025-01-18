from typing import Union

from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm

__all__ = ("AwsWaf",)


class AwsWaf(CaptchaParams):
    """
    The class is used to work with Capsolver AwsWaf methods:
     - AntiAwsWafTask
     - AntiAwsWafTaskProxyLess
     - AwsWafClassification

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``AntiAwsWafTask`` and etc.
        kwargs: additional params for client, like captcha waiting time
                    available keys:
                     - sleep_time: int - captcha solution waintig time in sec
                     - request_url: str - API address for sending requests,
                                            else official will be used


    Examples:
        >>> from python3_capsolver.aws_waf import AwsWaf
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> image = FileInstrument().file_processing(captcha_file="waf_captcha.png")
        >>>  AwsWaf(api_key="CAP-XXXXX",
        ...         captcha_type=CaptchaTypeEnm.AwsWafClassification
        ...         ).captcha_handler(task_payload={
        ...                                 "images": [image],
        ...                                 "question": "some question",
        ...                                 "websiteURL": "https://xxxx.com",
        ...                         })
        {
            "errorId":0,
            "errorCode":"None",
            "errorDescription":"None",
            "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
            "status":"ready",
            "solution":{
                //carcity point
                "box": [
                    116.7,
                    164.1
                ],
                // grid type, objects means the image index that matches the question
                "objects": [0, 1, 3, 4, 6],
                //if question include `bifurcatedzoo`
                "distance": 500
            }
        }


        >>> import asyncio
        >>> from python3_capsolver.aws_waf import AwsWaf
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> image = FileInstrument().file_processing(captcha_file="waf_captcha.png")
        >>> asyncio.run(AwsWaf(api_key="CAP-XXXXX",
        ...         captcha_type=CaptchaTypeEnm.AwsWafClassification
        ...         ).aio_captcha_handler(task_payload={
        ...                                 "images": [image],
        ...                                 "question": "some question",
        ...                                 "websiteURL": "https://xxxx.com",
        ...                         }))
        {
            "errorId":0,
            "errorCode":"None",
            "errorDescription":"None",
            "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
            "status":"ready",
            "solution":{
                //carcity point
                "box": [
                    116.7,
                    164.1
                ],
                // grid type, objects means the image index that matches the question
                "objects": [0, 1, 3, 4, 6],
                //if question include `bifurcatedzoo`
                "distance": 500
            }
        }

        >>> from python3_capsolver.aws_waf import AwsWaf
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> image = FileInstrument().file_processing(captcha_file="waf_captcha.png")
        >>>  AwsWaf(api_key="CAP-XXXXX",
        ...         captcha_type=CaptchaTypeEnm.AntiAwsWafTaskProxyLess
        ...         ).captcha_handler(task_payload={
        ...                                 "websiteURL": "https://xxxxxx/latest",
        ...                                 "awsKey": "AQIDAHjcYu/GjX+QlghicBg......shMIKvZswZemrVVqA==",
        ...                                 "awsChallengeJS": "https://xxxxx/challenge.js",
        ...                         })
        {
            "errorId":0,
            "errorCode":"None",
            "errorDescription":"None",
            "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
            "status":"ready",
            "solution":{
                "cookie": "223d1f60-xxxxxxxx"
            }
        }

        >>> from python3_capsolver.aws_waf import AwsWaf
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> image = FileInstrument().file_processing(captcha_file="waf_captcha.png")
        >>>  AwsWaf(api_key="CAP-XXXXX",
        ...         captcha_type=CaptchaTypeEnm.AntiAwsWafTask
        ...         ).captcha_handler(task_payload={
        ...                                 "websiteURL": "https://xxxxxx/latest",
        ...                                 "awsKey": "AQIDAHjcYu/GjX+QlghicBg......shMIKvZswZemrVVqA==",
        ...                                 "awsChallengeJS": "https://xxxxx/challenge.js",
        ...                                 "proxy": "ip:port:user:pass"
        ...                         })
        {
            "errorId":0,
            "errorCode":"None",
            "errorDescription":"None",
            "taskId":"db0a3153-621d-4f5e-8554-a1c032597ee7",
            "status":"ready",
            "solution":{
                "cookie": "223d1f60-xxxxxxxx"
            }
        }

    Notes:
        https://docs.capsolver.com/en/guide/captcha/awsWaf/

        https://docs.capsolver.com/en/guide/recognition/AwsWafClassification/
    """

    def __init__(self, api_key: str, captcha_type: Union[CaptchaTypeEnm, str], **kwargs):

        super().__init__(api_key=api_key, captcha_type=captcha_type, **kwargs)
