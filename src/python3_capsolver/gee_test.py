from typing import Union

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import GeeTestCaptchaTypeEnm
from python3_capsolver.core.serializer import GeeTestSer, CaptchaResponseSer


class GeeTest(BaseCaptcha):
    """
    The class is used to work with Capsolver GeeTestTask methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``GeeTestTaskProxyLess`` and etc.
        websiteURL: Address of a webpage with Geetest
        gt: The domain public key, rarely updated
        challenge: If you need to solve Geetest V3 you must use this parameter, don't need if you need to solve GeetestV4

    Examples:
        >>> GeeTest(api_key="CAI-1324...",
        ...         captcha_type=GeeTestCaptchaTypeEnm.GeeTestTaskProxyLess,
        ...         websiteURL="https://www.geetest.com/en/demo",
        ...         gt="022397c99c9f646f6477822485f30404",
        ...         challenge='12345678abc90123d45678ef90123a456b'
        ...        ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> GeeTest(api_key="CAI-1324...",
        ...         captcha_type=GeeTestCaptchaTypeEnm.GeeTestTask,
        ...         websiteURL="https://www.geetest.com/en/demo",
        ...         gt="022397c99c9f646f6477822485f30404",
        ...         challenge='12345678abc90123d45678ef90123a456b'
        ...         proxy="socks5:192.191.100.10:4780:user:pwd"
        ...        ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> await GeeTest(api_key="CAI-1324...",
        ...         captcha_type="GeetestTaskProxyless",
        ...         websiteURL="https://www.geetest.com/en/demo",
        ...         gt="022397c99c9f646f6477822485f30404",
        ...         challenge='12345678abc90123d45678ef90123a456b'
        ...        ).aio_captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )


    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://docs.capsolver.com/guide/captcha/Geetest.html
    """

    def __init__(
        self, captcha_type: Union[GeeTestCaptchaTypeEnm, str], websiteURL: str, gt: str, challenge: str, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        if captcha_type in GeeTestCaptchaTypeEnm.list():
            self.task_params = GeeTestSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {GeeTestCaptchaTypeEnm.list()}"""
            )
        for key in kwargs:
            self.task_params.update({key: kwargs[key]})

    def captcha_handler(self) -> CaptchaResponseSer:
        """
        Sync solving method

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        return self._processing_captcha(create_params=self.task_params)

    async def aio_captcha_handler(self) -> CaptchaResponseSer:
        """
        Async  solving method

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        return await self._aio_processing_captcha(create_params=self.task_params)
