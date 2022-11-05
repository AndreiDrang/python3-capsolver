from typing import Union

from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enums import ProxyType, CaptchaTypeEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import (
    CaptchaResponseSer,
    RequestCreateTaskSer,
    ReCaptchaV2OptionsSer,
    ReCaptchaV2ProxyLessOptionsSer,
)


class BaseReCaptcha(BaseCaptcha):
    """
    The class is used to work with CaptchaAI ReCaptcha methods.

    Args:
        api_key: CaptchaAI API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        websiteURL: Address of a webpage with Google ReCaptcha
        websiteKey: Recaptcha website key. <div class="g-recaptcha" data-sitekey="THAT_ONE"></div>
        proxyType: Type of the proxy
        proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                        host names instead of IPs,
                        transparent proxies (where client IP is visible),
                        proxies from local networks (192.., 10.., 127...)
        proxyPort: Proxy port.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests

    Examples:
        >>> ReCaptcha(api_key="CAI-1324...", \
                        captcha_type="ReCaptchaV2TaskProxyLess", \
                        websiteURL="https://rucaptcha.com/demo/recaptcha-v2", \
                        websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH" \
                        ).captcha_handler()

        CaptchaResponseSer(errorId=False
                            ErrorCode=None
                            errorDescription=None
                            taskId=None
                            status=<ResponseStatusEnm.Ready: 'ready'>
                            solution={'gRecaptchaResponse': '44795sds'}
                        )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/393446/ReCaptchaV2TaskProxyLess+solving+Google+recaptcha
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426184/ReCaptchaV2Task+solving+Google+recaptcha
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/393981/ReCaptchaV2EnterpriseTask+solving+Google+reCAPTCHA+Enterprise
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426203/ReCaptchaV2EnterpriseTaskProxyless+solving+Google+reCAPTCHA+Enterprise
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        websiteKey: str,
        proxyType: Union[ProxyType, str] = None,
        proxyAddress: str = None,
        proxyPort: int = None,
        sleep_time: int = 5,
        request_url: str = REQUEST_URL,
    ):

        super().__init__(api_key=api_key, sleep_time=sleep_time, request_url=request_url, captcha_type=captcha_type)

        # validation of the received parameters for ProxyLess captcha
        if self.captcha_type in (
            CaptchaTypeEnm.ReCaptchaV2TaskProxyLess,
            CaptchaTypeEnm.ReCaptchaV2EnterpriseTaskProxyless,
        ):
            ReCaptchaV2ProxyLessOptionsSer(**locals())
        # validation of the received parameters for captcha with Proxy params
        elif self.captcha_type in (CaptchaTypeEnm.ReCaptchaV2Task, CaptchaTypeEnm.ReCaptchaV2EnterpriseTask):
            ReCaptchaV2OptionsSer(**locals())
        else:
            raise ValueError(
                f"Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,"
                f"available - {CaptchaTypeEnm.ReCaptchaV2TaskProxyLess.value, CaptchaTypeEnm.ReCaptchaV2Task.value}"
            )

        self.task_params = dict(
            websiteURL=websiteURL,
            websiteKey=websiteKey,
            proxyType=proxyType,
            proxyAddress=proxyAddress,
            proxyPort=proxyPort,
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
                                and will be passed to the payload under `task` key.
                                Like `recaptchaDataSValue`, `isInvisible`, `userAgent`, `cookies`,
                                `proxyLogin`, `proxyPassword` - more info in service docs

        Examples:
            >>> ReCaptcha(api_key="CAI-1324...", \
                            captcha_type="ReCaptchaV2TaskProxyLess", \
                            websiteURL="https://rucaptcha.com/demo/recaptcha-v2", \
                            websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH" \
                            ).captcha_handler()

            CaptchaResponseSer(errorId=False
                                ErrorCode=None
                                errorDescription=None
                                taskId=None
                                status=<ResponseStatusEnm.Ready: 'ready'>
                                solution={'gRecaptchaResponse': '44795sds'}
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
                                and will be passed to the payload under `task` key.
                                Like `recaptchaDataSValue`, `isInvisible`, `userAgent`, `cookies`,
                                `proxyLogin`, `proxyPassword` - more info in service docs

        Examples:
            >>> await ReCaptcha(api_key="CAI-1324...", \
                            captcha_type="ReCaptchaV2TaskProxyLess", \
                            websiteURL="https://rucaptcha.com/demo/recaptcha-v2", \
                            websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH" \
                            ).aio_captcha_handler()

            CaptchaResponseSer(errorId=False
                                ErrorCode=None
                                errorDescription=None
                                taskId=None
                                status=<ResponseStatusEnm.Ready: 'ready'>
                                solution={'gRecaptchaResponse': '44795sds'}
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
