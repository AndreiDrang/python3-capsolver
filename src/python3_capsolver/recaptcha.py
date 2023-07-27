from typing import Union, Optional

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import ReCaptchaV2TypeEnm, ReCaptchaV3TypeEnm
from python3_capsolver.core.serializer import ReCaptchaV3Ser, CaptchaResponseSer, WebsiteDataOptionsSer


class ReCaptcha(BaseCaptcha):
    """
    The class is used to work with Capsolver ReCaptcha methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``ReCaptchaV2Task`` and etc.
        websiteURL: Address of a webpage with Google ReCaptcha
        websiteKey: Recaptcha website key. <div class="g-recaptcha" data-sitekey="THAT_ONE"></div>
        pageAction: Widget action value. Website owner defines what user is doing on the page through this parameter.
                    Default value: ``verify``. Example: grecaptcha.execute('site_key', {action:'login_test'}).

    Examples:
        >>> ReCaptcha(api_key="CAI-1324...",
        ...           captcha_type="ReCaptchaV2TaskProxyLess",
        ...           websiteURL="https://www.google.com/recaptcha/api2/demo",
        ...           websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
        ...          ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> ReCaptcha(api_key="CAI-1324...",
        ...           captcha_type=ReCaptchaV2TypeEnm.ReCaptchaV2TaskProxyLess,
        ...           websiteURL="https://www.google.com/recaptcha/api2/demo",
        ...           websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
        ...          ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> ReCaptcha(api_key="CAI-1324...",
        ...           captcha_type=ReCaptchaV2TypeEnm.ReCaptchaV2Task,
        ...           websiteURL="https://www.google.com/recaptcha/api2/demo",
        ...           websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        ...           proxy="socks5:192.191.100.10:4780:user:pwd"
        ...          ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> ReCaptcha(api_key="CAI-1324...",
        ...           captcha_type=ReCaptchaV3TypeEnm.ReCaptchaV3TaskProxyLess,
        ...           websiteURL="https://2captcha.com/demo/recaptcha-v3",
        ...           websiteKey="6LfB5_IbAAAAAMCtsjEHEHKqcB9iQocwwxTiihJu",
        ...           pageAction="demo_action",
        ...           proxy="socks5:192.191.100.10:4780:user:pwd"
        ...          ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> await ReCaptcha(api_key="CAI-1324...",
        ...           captcha_type=ReCaptchaV3TypeEnm.ReCaptchaV3TaskProxyLess,
        ...           websiteURL="https://2captcha.com/demo/recaptcha-v3",
        ...           websiteKey="6LfB5_IbAAAAAMCtsjEHEHKqcB9iQocwwxTiihJu",
        ...           pageAction="demo_action",
        ...           proxy="socks5:192.191.100.10:4780:user:pwd"
        ...          ).aio_captcha_handler()
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
        https://docs.capsolver.com/guide/captcha/ReCaptchaV2.html
        https://docs.capsolver.com/guide/captcha/ReCaptchaV3.html
    """

    def __init__(
        self,
        captcha_type: Union[ReCaptchaV2TypeEnm, ReCaptchaV3TypeEnm, str],
        websiteURL: str,
        websiteKey: str,
        pageAction: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if captcha_type in ReCaptchaV2TypeEnm.list():
            self.task_params = WebsiteDataOptionsSer(**locals()).dict()
        elif captcha_type in ReCaptchaV3TypeEnm.list():
            self.task_params = ReCaptchaV3Ser(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {ReCaptchaV2TypeEnm.list(), ReCaptchaV3TypeEnm.list()}"""
            )
        for key in kwargs:
            self.task_params.update({key: kwargs[key]})

    def captcha_handler(self) -> CaptchaResponseSer:
        """
        Sync method for captcha solving

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        return self._processing_captcha(create_params=self.task_params)

    async def aio_captcha_handler(self) -> CaptchaResponseSer:
        """
        Async method for captcha solving


        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        return await self._aio_processing_captcha(create_params=self.task_params)
