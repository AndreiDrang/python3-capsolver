from typing import List, Union

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import HCaptchaTypeEnm, HCaptchaClassificationTypeEnm
from python3_capsolver.core.serializer import (
    CaptchaResponseSer,
    WebsiteDataOptionsSer,
    HCaptchaClassificationOptionsSer,
)


class HCaptcha(BaseCaptcha):
    """
    The class is used to work with Capsolver HCaptcha methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``HCaptchaTaskProxyless`` and etc.
        websiteURL: Address of a webpage with hCaptcha
        websiteKey: hCaptcha website key

    Examples:
        >>> HCaptcha(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type='HCaptchaTaskProxyless',
        ...          websiteURL="https://accounts.hcaptcha.com/demo",
        ...          websiteKey="a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> HCaptcha(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=HCaptchaTypeEnm.HCaptchaEnterpriseTaskProxyLess,
        ...          websiteURL="https://accounts.hcaptcha.com/demo",
        ...          websiteKey="a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> HCaptcha(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=HCaptchaTypeEnm.HCaptchaTask,
        ...          websiteURL="https://accounts.hcaptcha.com/demo",
        ...          websiteKey="a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
        ...          proxy="socks5:192.191.100.10:4780:user:pwd"
        ...          isInvisible=True
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> await HCaptcha(api_key="CAI-BA9650D2B9C2786B21120D512702E010",
        ...          captcha_type=HCaptchaTypeEnm.HCaptchaTaskProxyless,
        ...          websiteURL="https://accounts.hcaptcha.com/demo",
        ...          websiteKey="a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
        ...         ).aio_captcha_handler()
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
        https://docs.capsolver.com/guide/captcha/HCaptcha.html
    """

    def __init__(self, captcha_type: Union[HCaptchaTypeEnm, str], websiteURL: str, websiteKey: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if captcha_type in HCaptchaTypeEnm.list():
            self.task_params = WebsiteDataOptionsSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {HCaptchaTypeEnm.list_values()}"""
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
        Async method for captcha solving

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        return await self._aio_processing_captcha(create_params=self.task_params)


class HCaptchaClassification(BaseCaptcha):
    """
    The class is used to work with Capsolver HCaptchaClassification methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``HCaptchaClassification`` and etc.
        queries: Base64 encoded image, do not include "data:image/***; base64," Assembles the picture as a list: [base64,base64,base64...]
        question: English is supported only. Please convert other languages by yourself

    Examples:
        >>> HCaptchaClassification(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type='HCaptchaClassification',
        ...          images=["/9j/4AAQS.....", "/9j/4AAQ2.....",],
        ...          question="Please click each image containing a chair",
        ...         ).captcha_handler()
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
        https://docs.capsolver.com/guide/recognition/HCaptchaClassification.html
    """

    def __init__(
        self,
        queries: List[str],
        question: str,
        captcha_type: Union[HCaptchaClassificationTypeEnm, str] = HCaptchaClassificationTypeEnm.HCaptchaClassification,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if captcha_type in HCaptchaClassificationTypeEnm.list():
            self.task_params = HCaptchaClassificationOptionsSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {HCaptchaClassificationTypeEnm.list_values()}"""
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
        Async method for captcha solving

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        return await self._aio_processing_captcha(create_params=self.task_params)
