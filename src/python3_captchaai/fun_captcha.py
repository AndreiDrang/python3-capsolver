from typing import Union, Optional

from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enum import ProxyType, CaptchaTypeEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import (
    CaptchaResponseSer,
    FunCaptchaOptionsSer,
    RequestCreateTaskSer,
    FunCaptchaProxyLessOptionsSer,
)


class BaseFunCaptcha(BaseCaptcha):
    """
    The class is used to work with CaptchaAI FuncaptchaTask methods.

    Args:
        api_key: CaptchaAI API key
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
        self,
        api_key: str,
        captcha_type: Union[CaptchaTypeEnm, str],
        websiteURL: Optional[str] = None,
        websitePublicKey: Optional[str] = None,
        funcaptchaApiJSSubdomain: Optional[str] = None,
        proxyType: Optional[Union[ProxyType, str]] = None,
        proxyAddress: Optional[str] = None,
        proxyPort: Optional[int] = None,
        sleep_time: Optional[int] = 5,
        request_url: Optional[str] = REQUEST_URL,
    ):
        super().__init__(api_key=api_key, captcha_type=captcha_type, sleep_time=sleep_time, request_url=request_url)

        # validation of the received parameters for FuncaptchaTaskProxyless
        if self.captcha_type == CaptchaTypeEnm.FuncaptchaTaskProxyless:
            self.task_params = FunCaptchaProxyLessOptionsSer(**locals()).dict()
        # validation of the received parameters for FuncaptchaTask
        elif self.captcha_type == CaptchaTypeEnm.FuncaptchaTask:
            self.task_params = FunCaptchaOptionsSer(**locals()).dict()
        # validation of the received parameters for FunCaptchaClassification
        elif self.captcha_type == CaptchaTypeEnm.FunCaptchaClassification:
            self.task_params = {}
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {CaptchaTypeEnm.FuncaptchaTaskProxyless.value,
                             CaptchaTypeEnm.FuncaptchaTask.value,
                             CaptchaTypeEnm.FunCaptchaClassification.value}"""
            )


class FunCaptcha(BaseFunCaptcha):
    __doc__ = BaseFunCaptcha.__doc__

    def captcha_handler(
        self,
        image: Optional[str] = None,
        question: Optional[str] = None,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            image: Base64 encoded image, can be a screenshot
                    (pass only the hexagonal image, do not pass the rest of the content)
            question: Question name. Pass the full name, such as: Pick the lion
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``data``, ``proxyLogin`` and etc. - more info in service docs

        Examples:
            >>> FunCaptcha(api_key="CAI-1324...",
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

            >>> FunCaptcha(api_key="CAI-1324...",
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

            >>> with open('some_image.jpeg', 'rb') as img_file:
            ...    img_data = img_file.read()
            >>> body = base64.b64encode(img_data).decode("utf-8")
            >>> FunCaptcha(api_key="CAI-1324...",
            ...         captcha_type="FunCaptchaClassification"
            ...        ).captcha_handler(
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
        # validation of the received parameters for FunCaptchaClassification
        if self.captcha_type == CaptchaTypeEnm.FunCaptchaClassification:
            if not image or not question:
                raise ValueError(
                    f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                    available - {CaptchaTypeEnm.FuncaptchaTaskProxyless.value,
                                 CaptchaTypeEnm.FuncaptchaTask.value,
                                 CaptchaTypeEnm.FunCaptchaClassification.value}"""
                )
            self.task_params.update({"image": image, "question": question})

        self.task_params.update({**additional_params})
        return self._processing_captcha(serializer=RequestCreateTaskSer, type=self.captcha_type, **self.task_params)

    async def aio_captcha_handler(
        self,
        image: Optional[str] = None,
        question: Optional[str] = None,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Asynchronous method for captcha solving

        Args:
            image: Base64 encoded image, can be a screenshot
                    (pass only the hexagonal image, do not pass the rest of the content)
            question: Question name. Pass the full name, such as: Pick the lion
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``coordinate``, ``enterprisePayload`` and etc. - more info in service docs

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
        # validation of the received parameters for FunCaptchaClassification
        if self.captcha_type == CaptchaTypeEnm.FunCaptchaClassification:
            if not image or not question:
                raise ValueError(
                    f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                    available - {CaptchaTypeEnm.FuncaptchaTaskProxyless.value,
                                 CaptchaTypeEnm.FuncaptchaTask.value,
                                 CaptchaTypeEnm.FunCaptchaClassification.value}"""
                )
            self.task_params.update({"image": image, "question": question})

        self.task_params.update({**additional_params})
        return await self._aio_processing_captcha(
            serializer=RequestCreateTaskSer, type=self.captcha_type, **self.task_params
        )
