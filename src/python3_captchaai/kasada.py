from typing import Union, Optional

from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enum import ProxyType, CaptchaTypeEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import KasadaOptionsSer, CaptchaResponseSer, RequestCreateTaskSer


class BaseKasada(BaseCaptcha):
    """
    The class is used to work with Capsolver AntiKasadaTask methods.

    Args:
        api_key: Capsolver API key
        pageURL: Address of a webpage with Kasada
        proxyType: Type of the proxy
        proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                        host names instead of IPs,
                        transparent proxies (where client IP is visible),
                        proxies from local networks (192.., 10.., 127...)
        proxyPort: Proxy port.
        proxyLogin: Login for proxy which requires authorizaiton (basic).
                        This isn’t required if you are using proxies authenticated by IP
        proxyPassword: This isn’t required if you are using proxies authenticated by IP
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests

    Examples:
        >>> Kasada(api_key="CAI-1324...",
        ...         pageURL="http://mywebsite.com/kasada",
        ...         proxyType="http",
        ...         proxyAddress="0.0.0.0",
        ...         proxyPort=9090,
        ...         proxyLogin="some_login",
        ...         proxyPassword="some_password",
        ...        ).captcha_handler()
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={
                               "x-kpsdk-ct": "",
                                "x-kpsdk-cd": "",
                                "user-agent": "Mozilla/5.0 (Windows NT 10...."
                            }
                          )

        >>> Kasada(api_key="CAI-1324...",
        ...         pageURL="http://mywebsite.com/kasada",
        ...         proxyType="http",
        ...         proxyAddress="0.0.0.0",
        ...         proxyPort=9090,
        ...         proxyLogin="some_login",
        ...         proxyPassword="some_password",
        ...        ).captcha_handler(userAgent="Mozilla/5.0 (pl.....")
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={
                               "x-kpsdk-ct": "",
                                "x-kpsdk-cd": "",
                                "user-agent": "Mozilla/5.0 (Windows NT 10...."
                            }
                          )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426407
    """

    def __init__(
        self,
        api_key: str,
        pageURL: str,
        proxyType: Union[ProxyType, str],
        proxyAddress: str,
        proxyPort: int,
        proxyLogin: str,
        proxyPassword: str,
        sleep_time: Optional[int] = 5,
        request_url: Optional[str] = REQUEST_URL,
    ):
        self.task_postfix = "/kasada/invoke"

        super().__init__(
            api_key=api_key, captcha_type=CaptchaTypeEnm.AntiKasadaTask, sleep_time=sleep_time, request_url=request_url
        )

        self.task_params = KasadaOptionsSer(**locals()).dict()


class Kasada(BaseKasada):
    __doc__ = BaseKasada.__doc__

    def captcha_handler(self, **additional_params) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``onlyCD``, ``userAgent`` and etc. - more info in service docs

        Examples:
            >>> Kasada(api_key="CAI-1324...",
            ...         pageURL="http://mywebsite.com/kasada",
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9090,
            ...         proxyLogin="some_login",
            ...         proxyPassword="some_password",
            ...        ).captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={
                                   "x-kpsdk-ct": "",
                                    "x-kpsdk-cd": "",
                                    "user-agent": "Mozilla/5.0 (Windows NT 10...."
                                }
                              )

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstirng for more info
        """
        self.task_params.update({**additional_params})
        self._prepare_create_task_payload(serializer=RequestCreateTaskSer, create_params=self.task_params)
        return CaptchaResponseSer(**self._create_task(url_postfix=self.task_postfix))

    async def aio_captcha_handler(self, **additional_params) -> CaptchaResponseSer:
        """
        Asynchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``onlyCD``, ``userAgent`` and etc. - more info in service docs

        Examples:
            >>> await Kasada(api_key="CAI-1324...",
            ...         pageURL="http://mywebsite.com/kasada",
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9090,
            ...         proxyLogin="some_login",
            ...         proxyPassword="some_password",
            ...        ).aio_captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={
                                   "x-kpsdk-ct": "",
                                    "x-kpsdk-cd": "",
                                    "user-agent": "Mozilla/5.0 (Windows NT 10...."
                                }
                              )

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstirng for more info
        """
        self.task_params.update({**additional_params})
        self._prepare_create_task_payload(serializer=RequestCreateTaskSer, create_params=self.task_params)
        return CaptchaResponseSer(**await self._aio_create_task(url_postfix=self.task_postfix))
