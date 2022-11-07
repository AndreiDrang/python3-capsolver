from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enum import CaptchaTypeEnm, EndpointPostfixEnm
from python3_captchaai.core.config import REQUEST_URL
from python3_captchaai.core.serializer import PostRequestSer, ControlResponseSer


class BaseControl(BaseCaptcha):
    """
    Args:
        api_key: CaptchaAI API key
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

    serializer = PostRequestSer

    def __init__(
        self,
        api_key: str,
        sleep_time: int = 10,
        request_url: str = REQUEST_URL,
    ):

        super().__init__(
            api_key=api_key, sleep_time=sleep_time, request_url=request_url, captcha_type=CaptchaTypeEnm.Control
        )


class Control(BaseControl):
    """
    The class is used to work with CaptchaAI control methods.

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426042/API+Methods
    """

    def get_balance(self) -> ControlResponseSer:
        """
        Synchronous method to view the balance

        Examples:
            >>> Control(api_key="CAI-12345").get_balance()
            ResponseSer(balance=1.0 errorId=False errorCode=None errorDescription=None)

        Returns:
            ResponseSer model with full server response

        Notes:
            https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426080/getBalance+retrieve+account+balance
        """
        self._prepare_create_task_payload(serializer=self.serializer)
        return ControlResponseSer(
            **self._create_task(
                url_postfix=EndpointPostfixEnm.GET_BALANCE.value,
            )
        )

    async def aio_get_balance(self) -> ControlResponseSer:
        """
        Asynchronous method to view the balance

        Examples:
            >>> await Control(api_key="CAI-12345").aio_get_balance()
            ResponseSer(balance=1.0 errorId=False errorCode=None errorDescription=None)

        Returns:
            ResponseSer model with full server response

        Notes:
            https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426080/getBalance+retrieve+account+balance
        """
        self._prepare_create_task_payload(serializer=self.serializer)
        return ControlResponseSer(
            **await self._aio_create_task(
                url_postfix=EndpointPostfixEnm.GET_BALANCE.value,
            )
        )
