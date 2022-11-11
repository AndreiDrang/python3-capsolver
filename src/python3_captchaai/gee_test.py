from typing import Union, Optional

from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enum import ProxyType, CaptchaTypeEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import (
    GeeTestOptionsSer,
    CaptchaResponseSer,
    RequestCreateTaskSer,
    GeeTestProxyLessOptionsSer,
)


class BaseGeeTest(BaseCaptcha):
    """
    The class is used to work with CaptchaAI GeetestTask methods.

    Args:
        api_key: CaptchaAI API key
        captcha_type: Captcha type name, like ``GeetestTaskProxyless`` and etc.
        websiteURL: Address of a webpage with Geetest
        gt: The domain public key, rarely updated
        proxyType: Type of the proxy
        proxyAddress: Proxy IP address IPv4/IPv6. Not allowed to use:
                        host names instead of IPs,
                        transparent proxies (where client IP is visible),
                        proxies from local networks (192.., 10.., 127...)
        proxyPort: Proxy port.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests

    Examples:
        >>> GeeTest(api_key="CAI-1324...",
        ...         captcha_type="GeetestTaskProxyless",
        ...         websiteURL="https://www.geetest.com/en/demo",
        ...         gt="022397c99c9f646f6477822485f30404",
        ...        ).captcha_handler(
        ...                    challenge="a66f31a53a404af8d1f271eec5138aa1",
        ...                    geetestApiServerSubdomain="api.geetest.com"
        ...                )
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
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/394048
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426338
    """

    def __init__(
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: str,
        gt: str,
        proxyType: Optional[Union[ProxyType, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        sleep_time: Optional[int] = 5,
        request_url: Optional[str] = REQUEST_URL,
    ):

        super().__init__(api_key=api_key, captcha_type=captcha_type, sleep_time=sleep_time, request_url=request_url)

        # validation of the received parameters for GeetestTaskProxyless
        if self.captcha_type == CaptchaTypeEnm.GeetestTaskProxyless:
            self.task_params = GeeTestProxyLessOptionsSer(**locals()).dict()
        # validation of the received parameters for GeetestTask
        elif self.captcha_type == CaptchaTypeEnm.GeetestTask:
            self.task_params = GeeTestOptionsSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {CaptchaTypeEnm.GeetestTaskProxyless.value,
                             CaptchaTypeEnm.GeetestTask.value}"""
            )


class GeeTest(BaseGeeTest):
    __doc__ = BaseGeeTest.__doc__

    def captcha_handler(
        self,
        challenge: str,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            challenge: Changing token key.
                        Make sure you grab a fresh one for each captcha;
                        otherwise, you'll be charged for an error task.
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``coordinate``, ``enterprisePayload`` and etc. - more info in service docs

        Examples:
            >>> GeeTest(api_key="CAI-1324...",
            ...         captcha_type="GeetestTaskProxyless",
            ...         websiteURL="https://www.geetest.com/en/demo",
            ...         gt="022397c99c9f646f6477822485f30404",
            ...        ).captcha_handler(
            ...                    challenge="a66f31a53a404af8d1f271eec5138aa1",
            ...                    geetestApiServerSubdomain="api.geetest.com"
            ...                )
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
        self.task_params.update({**additional_params, "challenge": challenge})
        return self._processing_captcha(serializer=RequestCreateTaskSer, type=self.captcha_type, **self.task_params)

    async def aio_captcha_handler(
        self,
        challenge: str,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Asynchronous method for captcha solving

        Args:
            challenge: Changing token key.
                        Make sure you grab a fresh one for each captcha;
                        otherwise, you'll be charged for an error task.
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``coordinate``, ``enterprisePayload`` and etc. - more info in service docs

        Examples:
            >>> await GeeTest(api_key="CAI-1324...",
            ...                 captcha_type="GeetestTaskProxyless",
            ...                 websiteURL="https://www.geetest.com/en/demo",
            ...                 gt="022397c99c9f646f6477822485f30404",
            ...             ).aio_captcha_handler(
            ...                    challenge="a66f31a53a404af8d1f271eec5138aa1",
            ...                    geetestApiServerSubdomain="api.geetest.com"
            ...                )
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
        self.task_params.update({**additional_params, "challenge": challenge})
        return await self._aio_processing_captcha(
            serializer=RequestCreateTaskSer, type=self.captcha_type, **self.task_params
        )
