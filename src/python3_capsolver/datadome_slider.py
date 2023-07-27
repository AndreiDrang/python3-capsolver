from typing import Union

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import DatadomeSliderTypeEnm
from python3_capsolver.core.serializer import DatadomeSliderSer, CaptchaResponseSer


class DatadomeSlider(BaseCaptcha):
    """
    The class is used to work with Capsolver DatadomeSlider method.

    Args:
        api_key: Capsolver API key
        websiteURL: Address of the webpage
        captchaUrl: Captcha Url where is the captcha
        proxy: Proxy data
        userAgent: Browser's User-Agent which is used in emulation

    Examples:
        >>> DatadomeSlider(api_key="CAI-1324...",
        ...         captcha_type=DatadomeSliderTypeEnm.DatadomeSliderTask,
        ...         websiteURL="https://www.some-url.com/",
        ...         captchaUrl="https://www.some-url.com/to-page-with-captcha",
        ...         proxy="socks5:158.120.100.23:334:user:pass",
        ...         userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        ...        ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> await DatadomeSlider(api_key="CAI-1324...",
        ...         captcha_type="DatadomeSliderTask",
        ...         websiteURL="https://www.some-url.com/",
        ...         captchaUrl="https://www.some-url.com/to-page-with-captcha",
        ...         proxy="socks5:158.120.100.23:334:user:pass",
        ...         userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
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
        https://docs.capsolver.com/guide/antibots/datadome.html
    """

    def __init__(
        self,
        websiteURL: str,
        captchaUrl: str,
        userAgent: str,
        captcha_type: Union[DatadomeSliderTypeEnm, str] = DatadomeSliderTypeEnm.DatadomeSliderTask,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if captcha_type in DatadomeSliderTypeEnm.list():
            self.task_params = DatadomeSliderSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {DatadomeSliderTypeEnm.list()}"""
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

    async def aio_captcha_handler(
        self,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Async method for captcha solving

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        return await self._aio_processing_captcha(create_params=self.task_params)
