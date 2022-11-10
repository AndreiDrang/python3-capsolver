from typing import Union, Optional

from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enum import ProxyType, CaptchaTypeEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import (
    CaptchaResponseSer,
    ProxyDataOptionsSer,
    RequestCreateTaskSer,
    ReCaptchaV3OptionsSer,
    WebsiteDataOptionsSer,
    ReCaptchaV3ProxyLessOptionsSer,
)


class BaseReCaptcha(BaseCaptcha):
    """
    The class is used to work with CaptchaAI ReCaptcha methods.

    Args:
        api_key: CaptchaAI API key
        captcha_type: Captcha type name, like ``ReCaptchaV2Task`` and etc.
        websiteURL: Address of a webpage with Google ReCaptcha
        websiteKey: Recaptcha website key. <div class="g-recaptcha" data-sitekey="THAT_ONE"></div>
        pageAction: Widget action value. Website owner defines what user is doing on the page through this parameter.
                    Default value: ``verify``. Example: grecaptcha.execute('site_key', {action:'login_test'}).
        proxyType: Type of the proxy
        proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                        host names instead of IPs,
                        transparent proxies (where client IP is visible),
                        proxies from local networks (192.., 10.., 127...)
        proxyPort: Proxy port.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests

    Examples:
        >>> ReCaptcha(api_key="CAI-1324...",
        ...           captcha_type="ReCaptchaV2TaskProxyLess",
        ...           websiteURL="https://www.google.com/recaptcha/api2/demo",
        ...           websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
        ...          ).captcha_handler()
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
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/393446
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426184
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/393981
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426203
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        websiteKey: str,
        pageAction: Optional[str] = None,
        proxyType: Optional[Union[ProxyType, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        sleep_time: Optional[int] = 5,
        request_url: Optional[str] = REQUEST_URL,
    ):

        super().__init__(api_key=api_key, sleep_time=sleep_time, request_url=request_url, captcha_type=captcha_type)

        # validation of the received parameters for ProxyLess ReCaptcha V2
        if self.captcha_type in (
            CaptchaTypeEnm.ReCaptchaV2TaskProxyLess,
            CaptchaTypeEnm.ReCaptchaV2EnterpriseTaskProxyless,
        ):
            self.task_params = WebsiteDataOptionsSer(**locals()).dict()
        # validation of the received parameters for ReCaptcha V2 with Proxy params
        elif self.captcha_type in (CaptchaTypeEnm.ReCaptchaV2Task, CaptchaTypeEnm.ReCaptchaV2EnterpriseTask):
            self.task_params = ProxyDataOptionsSer(**locals()).dict()
        # validation of the received parameters for ReCaptcha V3 with ProxyLess params
        elif self.captcha_type == CaptchaTypeEnm.ReCaptchaV3TaskProxyless:
            self.task_params = ReCaptchaV3ProxyLessOptionsSer(**locals()).dict()
        # validation of the received parameters for ReCaptcha V3 with Proxy params
        elif self.captcha_type == CaptchaTypeEnm.ReCaptchaV3Task:
            self.task_params = ReCaptchaV3OptionsSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {CaptchaTypeEnm.ReCaptchaV2TaskProxyLess.value, 
                             CaptchaTypeEnm.ReCaptchaV2EnterpriseTaskProxyless.value,
                             CaptchaTypeEnm.ReCaptchaV2Task.value,
                             CaptchaTypeEnm.ReCaptchaV2EnterpriseTask.value,
                             CaptchaTypeEnm.ReCaptchaV3TaskProxyless.value,
                             CaptchaTypeEnm.ReCaptchaV3Task.value}"""
            )


class ReCaptcha(BaseReCaptcha):
    __doc__ = BaseReCaptcha.__doc__

    def captcha_handler(
        self,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``recaptchaDataSValue``, ``isInvisible``, ``userAgent``, ``cookies``,
                                ``proxyLogin``, ``proxyPassword`` - more info in service docs

        Examples:
            >>> ReCaptcha(api_key="CAI-1324...",
            ...           captcha_type="ReCaptchaV2TaskProxyLess",
            ...           websiteURL="https://www.google.com/recaptcha/api2/demo",
            ...           websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
            ...          ).captcha_handler()
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
        self.task_params.update(additional_params)
        return self._processing_captcha(serializer=RequestCreateTaskSer, type=self.captcha_type, **self.task_params)

    async def aio_captcha_handler(
        self,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Asynchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``recaptchaDataSValue``, ``isInvisible``, ``userAgent``, ``cookies``,
                                ``proxyLogin``, ``proxyPassword`` - more info in service docs

        Examples:
            >>> await ReCaptcha(api_key="CAI-1324...",
            ...                 captcha_type="ReCaptchaV2TaskProxyLess",
            ...                 websiteURL="https://www.google.com/recaptcha/api2/demo",
            ...                 websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
            ...                ).aio_captcha_handler()
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
        self.task_params.update(additional_params)
        return await self._aio_processing_captcha(
            serializer=RequestCreateTaskSer, type=self.captcha_type, **self.task_params
        )
