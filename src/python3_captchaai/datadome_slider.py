from typing import Union, Optional

from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enum import ProxyType, CaptchaTypeEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import CaptchaResponseSer, RequestCreateTaskSer, DatadomeSliderOptionsSer


class BaseDatadomeSlider(BaseCaptcha):
    """
    The class is used to work with CaptchaAI DatadomeSlider method.

    Args:
        api_key: CaptchaAI API key
        websiteURL: Address of the webpage
        captchaUrl: Captcha Url where is the captcha
        proxyType: Type of the proxy
        proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                        host names instead of IPs,
                        transparent proxies (where client IP is visible),
                        proxies from local networks (192.., 10.., 127...)
        proxyPort: Proxy port.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests

    Examples:
        >>> DatadomeSlider(api_key="CAI-1324...",
        ...         websiteURL="https://www.some-url.com/",
        ...         captchaUrl="https://www.some-url.com/to-page-with-captcha",
        ...         proxyType="http",
        ...         proxyAddress="0.0.0.0",
        ...         proxyPort=9090,
        ...        ).captcha_handler()
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> await DatadomeSlider(api_key="CAI-1324...",
        ...         websiteURL="https://www.some-url.com/",
        ...         captchaUrl="https://www.some-url.com/to-page-with-captcha",
        ...         proxyType="http",
        ...         proxyAddress="0.0.0.0",
        ...         proxyPort=9090,
        ...        ).aio_captcha_handler()
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
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426393/
    """

    def __init__(
        self,
        api_key: str,
        websiteURL: str,
        captchaUrl: str,
        proxyType: Union[ProxyType, str],
        proxyAddress: str,
        proxyPort: int,
        sleep_time: Optional[int] = 5,
        request_url: Optional[str] = REQUEST_URL,
    ):

        super().__init__(
            api_key=api_key,
            captcha_type=CaptchaTypeEnm.DatadomeSliderTask,
            sleep_time=sleep_time,
            request_url=request_url,
        )

        self.task_params = DatadomeSliderOptionsSer(**locals()).dict()


class DatadomeSlider(BaseDatadomeSlider):
    __doc__ = BaseDatadomeSlider.__doc__

    def captcha_handler(
        self,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``proxyPassword``, ``userAgent`` and etc. - more info in service docs

        Examples:
            >>> DatadomeSlider(api_key="CAI-1324...",
            ...         websiteURL="https://www.some-url.com/",
            ...         captchaUrl="https://www.some-url.com/to-page-with-captcha",
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9090,
            ...        ).captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'gRecaptchaResponse': '44795sds...'}
                              )

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstirng for more info
        """
        return self._processing_captcha(serializer=RequestCreateTaskSer, type=self.captcha_type, **additional_params)

    async def aio_captcha_handler(
        self,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Asynchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``coordinate``, ``enterprisePayload`` and etc. - more info in service docs

        Examples:
            >>> await DatadomeSlider(api_key="CAI-1324...",
            ...         websiteURL="https://www.some-url.com/",
            ...         captchaUrl="https://www.some-url.com/to-page-with-captcha",
            ...         proxyType="http",
            ...         proxyAddress="0.0.0.0",
            ...         proxyPort=9090,
            ...        ).aio_captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'gRecaptchaResponse': '44795sds...'}
                              )

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstirng for more info
        """
        return await self._aio_processing_captcha(
            serializer=RequestCreateTaskSer, type=self.captcha_type, **additional_params
        )
