from typing import Union, Optional

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import FunCaptchaTypeEnm
from python3_capsolver.core.serializer import (
    CaptchaResponseSer,
    FunCaptchaSer,
    RequestCreateTaskSer,
)


class FunCaptcha(BaseCaptcha):
    """
    The class is used to work with Capsolver FuncaptchaTask methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``GeetestTaskProxyless`` and etc.
        websiteURL: Address of a webpage with Geetest.
        websitePublicKey: Funcaptcha website key.
        funcaptchaApiJSSubdomain: A special subdomain of funcaptcha.com,from which the JS captcha should be loaded.
                                    Most FunCaptcha installations work from shared domains.
        proxyType: Type of the proxy
        proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                        host names instead of IPs,
                        transparent proxies (where client IP is visible),
                        proxies from local networks (192.., 10.., 127...)
        proxyPort: Proxy port.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests

    Examples:
        >>> with FunCaptcha(api_key="CAI-1324...",
        ...             captcha_type="FuncaptchaTaskProxyless",
        ...             websiteURL="https://api.funcaptcha.com/fc/api/nojs/",
        ...             websitePublicKey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
        ...             funcaptchaApiJSSubdomain="https://api.funcaptcha.com/"
        ...         ) as instance:
        >>>     instance.captcha_handler()
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': '44795sds...'}
                          )

        >>> with FunCaptcha(api_key="CAI-1324...",
        ...             captcha_type="FuncaptchaTaskProxyless",
        ...             websiteURL="https://api.funcaptcha.com/fc/api/nojs/",
        ...             websitePublicKey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
        ...             funcaptchaApiJSSubdomain="https://api.funcaptcha.com/"
        ...         ) as instance:
        >>>     await instance.aio_captcha_handler()
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': '44795sds...'}
                          )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426302
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/394062
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426373
    """

    def __init__(
        self, captcha_type: Union[FunCaptchaSer, str], websiteURL: str, websitePublicKey: str, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        if captcha_type in FunCaptchaTypeEnm.list():
            self.task_params = FunCaptchaSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {FunCaptchaTypeEnm.list()}"""
            )
        for key in kwargs:
            self.task_params.update({key: kwargs[key]})

    def captcha_handler(
        self
    ) -> CaptchaResponseSer:
        """
        Sync solving method

        Examples:
            >>> FunCaptcha(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
            ...         captcha_type="FuncaptchaTaskProxyless",
            ...         websiteURL="https://api.funcaptcha.com/fc/api/nojs/",
            ...         websitePublicKey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            ...         funcaptchaApiJSSubdomain="https://api.funcaptcha.com/"
            ...        ).captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'token': '44795sds...'}
                              )

            >>> FunCaptcha(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
            ...         captcha_type="FuncaptchaTask",
            ...         websiteURL="https://api.funcaptcha.com/fc/api/nojs/",
            ...         websitePublicKey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            ...         funcaptchaApiJSSubdomain="https://api.funcaptcha.com/",
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9090,
            ...        ).captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'token': '44795sds...'}
                              )

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstirng for more info
        """
        return self._processing_captcha(create_params=self.task_params)

    async def aio_captcha_handler(
        self
    ) -> CaptchaResponseSer:
        """
        Async method for captcha solving

        Examples:
            >>> await FunCaptcha(api_key="CAI-1324...",
            ...         captcha_type="FuncaptchaTaskProxyless",
            ...         websiteURL="https://api.funcaptcha.com/fc/api/nojs/",
            ...         websitePublicKey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            ...         funcaptchaApiJSSubdomain="https://api.funcaptcha.com/"
            ...        ).aio_captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'token': '44795sds...'}
                              )

            >>> await FunCaptcha(api_key="CAI-1324...",
            ...         captcha_type="FuncaptchaTask",
            ...         websiteURL="https://api.funcaptcha.com/fc/api/nojs/",
            ...         websitePublicKey="69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            ...         funcaptchaApiJSSubdomain="https://api.funcaptcha.com/",
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9090,
            ...        ).aio_captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'token': '44795sds...'}
                              )

            >>> with open('some_image.jpeg', 'rb') as img_file:
            ...    img_data = img_file.read()
            >>> body = base64.b64encode(img_data).decode("utf-8")
            >>> await FunCaptcha(api_key="CAI-1324...",
            ...         captcha_type="FunCaptchaClassification"
            ...        ).aio_captcha_handler(
            ...                     image=body,
            ...                     question="Ask your question")
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'token': '44795sds...'}
                              )

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstirng for more info
        """
        return await self._aio_processing_captcha(create_params=self.task_params)
