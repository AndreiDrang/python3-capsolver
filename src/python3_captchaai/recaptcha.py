from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import CaptchaResponseSer, RequestCreateTaskSer


class BaseReCaptcha(BaseCaptcha):
    def __init__(self, api_key: str, captcha_type: str, sleep_time: int = 10, request_url: str = REQUEST_URL):
        super().__init__(api_key=api_key, sleep_time=sleep_time, request_url=request_url)

        self.captcha_type = captcha_type


class ReCaptcha(BaseReCaptcha):
    """
    The class is used to work with CaptchaAI control methods.

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/393427/ImageToTextTask+beta+solve+image+captcha
    """

    def captcha_handler(self, websiteURL: str, websiteKey: str, **additional_params) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            websiteURL: Address of a webpage with Google ReCaptcha
            websiteKey: Recaptcha website key. <div class="g-recaptcha" data-sitekey="THAT_ONE"></div>
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under `task` key.
                                Like `recaptchaDataSValue`, `isInvisible`, `userAgent`, `cookies`
                                - more info in service docs

        Examples:
            >>> ReCaptcha(api_key="CAI-1324...").captcha_handler(\
                                                    websiteURL="https://rucaptcha.com/demo/recaptcha-v2", \
                                                    websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH" \
                                                )

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
        """
        return self._processing_captcha(
            serializer=RequestCreateTaskSer,
            type=self.captcha_type,
            websiteURL=websiteURL,
            websiteKey=websiteKey,
            **additional_params,
        )

    async def aio_captcha_handler(self, websiteURL: str, websiteKey: str, **additional_params) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            websiteURL: Address of a webpage with Google ReCaptcha
            websiteKey: Recaptcha website key. <div class="g-recaptcha" data-sitekey="THAT_ONE"></div>
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under `task` key.
                                Like `recaptchaDataSValue`, `isInvisible`, `userAgent`, `cookies`
                                - more info in service docs

        Examples:
            >>> await ReCaptcha(api_key="CAI-1324...").aio_captcha_handler(\
                                                    websiteURL="https://rucaptcha.com/demo/recaptcha-v2", \
                                                    websiteKey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH" \
                                                )

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
        """
        return await self._aio_processing_captcha(
            serializer=RequestCreateTaskSer,
            type=self.captcha_type,
            websiteURL=websiteURL,
            websiteKey=websiteKey,
            **additional_params,
        )
