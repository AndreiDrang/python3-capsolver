from typing import Optional

from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enum import CaptchaTypeEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import CaptchaResponseSer, MtCaptchaOptionsSer, RequestCreateTaskSer


class BaseMtCaptcha(BaseCaptcha):
    """
    The class is used to work with Capsolver MtCaptcha method.

    Args:
        api_key: Capsolver API key
        websiteURL: Address of a webpage with mtcaptcha
        websiteKey: `sk=MTPublic-xxx` public key
        proxy: String with proxy connection params, example: `198.22.3.1:10001:user:pwd`
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests

    Examples:
        >>> MtCaptcha(api_key="CAI-1324...",
        ...         websiteURL="https://www.mtcaptcha.com/#mtcaptcha-demo",
        ...         websiteKey="MTPublic-tqNCRE0GS",
        ...         proxy="198.22.3.1:10001:user:pwd"
        ...        ).captcha_handler()
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': 'v1(03,79a,MTPublic-tqNCRE0GS,c9...'}
                          )

        >>> MtCaptcha(api_key="CAI-1324...",
        ...         websiteURL="https://www.mtcaptcha.com/#mtcaptcha-demo",
        ...         websiteKey="MTPublic-tqNCRE0GS",
        ...         proxy="198.22.3.1:10001:user:pwd"
        ...        ).captcha_handler(isInvisible=False, userAgent='Mozilla/5.0 (pl.....')
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': 'v1(03,79a,MTPublic-tqNCRE0GS,c9...'}
                          )

        >>> await MtCaptcha(api_key="CAI-1324...",
        ...         websiteURL="https://www.mtcaptcha.com/#mtcaptcha-demo",
        ...         websiteKey="MTPublic-tqNCRE0GS",
        ...         proxy="198.22.3.1:10001:user:pwd"
        ...        ).aio_captcha_handler()
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': 'v1(03,79a,MTPublic-tqNCRE0GS,c9...'}
                          )

        >>> await MtCaptcha(api_key="CAI-1324...",
        ...         websiteURL="https://www.mtcaptcha.com/#mtcaptcha-demo",
        ...         websiteKey="MTPublic-tqNCRE0GS",
        ...         proxy="198.22.3.1:10001:user:pwd"
        ...        ).aio_captcha_handler(isInvisible=False, userAgent='Mozilla/5.0 (pl.....')
        CaptchaResponseSer(errorId=False,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                            solution={'token': 'v1(03,79a,MTPublic-tqNCRE0GS,c9...'}
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
        websiteKey: str,
        proxy: str,
        sleep_time: Optional[int] = 5,
        request_url: Optional[str] = REQUEST_URL,
    ):

        super().__init__(
            api_key=api_key,
            captcha_type=CaptchaTypeEnm.MtCaptchaTask,
            sleep_time=sleep_time,
            request_url=request_url,
        )

        self.task_params = MtCaptchaOptionsSer(**locals()).dict()


class MtCaptcha(BaseMtCaptcha):
    __doc__ = BaseMtCaptcha.__doc__

    def captcha_handler(
        self,
        **additional_params,
    ) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``isInvisible``, ``userAgent`` and etc. - more info in service docs

        Examples:
            >>> MtCaptcha(api_key="CAI-1324...",
            ...         websiteURL="https://www.mtcaptcha.com/#mtcaptcha-demo",
            ...         websiteKey="MTPublic-tqNCRE0GS",
            ...         proxy="198.22.3.1:10001:user:pwd"
            ...        ).captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'token': 'v1(03,79a,MTPublic-tqNCRE0GS,c9...'}
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
                                Like ``isInvisible``, ``userAgent`` and etc. - more info in service docs

        Examples:
            >>> await MtCaptcha(api_key="CAI-1324...",
            ...         websiteURL="https://www.mtcaptcha.com/#mtcaptcha-demo",
            ...         websiteKey="MTPublic-tqNCRE0GS",
            ...         proxy="198.22.3.1:10001:user:pwd"
            ...        ).aio_captcha_handler()
            CaptchaResponseSer(errorId=False,
                               errorCode=None,
                               errorDescription=None,
                               taskId='73bdcd28-6c77-4414-8....',
                               status=<ResponseStatusEnm.Ready: 'ready'>,
                               solution={'token': 'v1(03,79a,MTPublic-tqNCRE0GS,c9...'}
                              )

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstirng for more info
        """
        return await self._aio_processing_captcha(
            serializer=RequestCreateTaskSer, type=self.captcha_type, **additional_params
        )
