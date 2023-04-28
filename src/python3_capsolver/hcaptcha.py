from typing import Union

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import HCaptchaTypeEnm
from python3_capsolver.core.serializer import CaptchaResponseSer, WebsiteDataOptionsSer


class HCaptcha(BaseCaptcha):
    """
    The class is used to work with Capsolver HCaptcha methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``HCaptchaTaskProxyless`` and etc.
        websiteURL: Address of a webpage with hCaptcha
        websiteKey: hCaptcha website key
        queries: Base64-encoded images, do not include "data : image / *** ; base64,".
                    Format to send: [“base64”,”base64”,”base64”,…..]
        question: Question ID. Support English and Chinese, other languages please convert yourself
        proxyType: Type of the proxy
        proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                        host names instead of IPs,
                        transparent proxies (where client IP is visible),
                        proxies from local networks (192.., 10.., 127...)
        proxyPort: Proxy port.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests

    Examples:
        >>> HCaptcha(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type='HCaptchaTaskProxyless',
        ...          websiteURL="https://accounts.hcaptcha.com/demo",
        ...          websiteKey="a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> HCaptcha(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type='HCaptchaTask',
        ...          websiteURL="https://accounts.hcaptcha.com/demo",
        ...          websiteKey="a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
        ...          proxy="socks5:192.191.100.10:4780:user:pwd"
        ...          isInvisible=True
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> await HCaptcha(api_key="CAI-BA9650D2B9C2786B21120D512702E010",
        ...          captcha_type='HCaptchaTaskProxyless',
        ...          websiteURL="https://accounts.hcaptcha.com/demo",
        ...          websiteKey="a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
        ...         ).aio_captcha_handler()
        CaptchaResponseSer(errorId=False,
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
