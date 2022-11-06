from typing import List, Union, Optional

from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enums import ProxyType, CaptchaTypeEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import (
    CaptchaResponseSer,
    HCaptchaOptionsSer,
    ProxyDataOptionsSer,
    RequestCreateTaskSer,
    WebsiteDataOptionsSer,
)


class BaseHCaptcha(BaseCaptcha):
    """
    The class is used to work with CaptchaAI HCaptcha methods.

    Args:
        api_key: CaptchaAI API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        websiteURL: Address of a webpage with hCaptcha
        websiteKey: hCaptcha website key
        proxyType: Type of the proxy
        queries: Base64-encoded images, do not include "data:image/***;base64,".
                    Format to send: [“base64”,”base64”,”base64”,…..]
        question: Question ID. Support English and Chinese, other languages please convert yourself
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
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426247/HCaptchaTask+solving+hCaptcha+puzzle+solving
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/394005/HCaptchaTaskProxyless+solving+hCaptcha+puzzle+solving
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426261/HCaptchaClassification+recognize+the+images+that+you+need+to+click
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        websiteKey: str,
        queries: Optional[List[str]] = None,
        question: Optional[str] = None,
        proxyType: Optional[Union[ProxyType, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        sleep_time: Optional[int] = 5,
        request_url: Optional[str] = REQUEST_URL,
    ):

        super().__init__(api_key=api_key, sleep_time=sleep_time, request_url=request_url, captcha_type=captcha_type)

        # validation of the received parameters for HCaptchaTaskProxyless
        if self.captcha_type == CaptchaTypeEnm.HCaptchaTaskProxyless:
            self.task_params = WebsiteDataOptionsSer(**locals()).dict()
        # validation of the received parameters for HCaptchaTask
        elif self.captcha_type == CaptchaTypeEnm.HCaptchaTask:
            self.task_params = ProxyDataOptionsSer(**locals()).dict()
        # validation of the received parameters for HCaptchaClassification
        elif self.captcha_type == CaptchaTypeEnm.HCaptchaClassification:
            self.task_params = HCaptchaOptionsSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {CaptchaTypeEnm.HCaptchaTaskProxyless.value,
                             CaptchaTypeEnm.HCaptchaTask.value,
                             CaptchaTypeEnm.HCaptchaClassification.value}"""
            )


class HCaptcha(BaseHCaptcha):
    __doc__ = BaseHCaptcha.__doc__

    def captcha_handler(
        self,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under `task` key.
                                Like `coordinate`, `enterprisePayload` and etc. - more info in service docs

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
                                Like `coordinate`, `enterprisePayload` and etc. - more info in service docs

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