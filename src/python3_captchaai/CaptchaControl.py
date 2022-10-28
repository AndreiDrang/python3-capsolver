from .base import BaseCaptcha
from .enums import CaptchaControlEnm
from .serializer import ResponseSer


class BaseCaptchaControl(BaseCaptcha):
    pass


class CaptchaControl(BaseCaptchaControl):
    """
    The class is used to work with CaptchaAI control methods.

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426042/API+Methods
    """

    def get_balance(self) -> ResponseSer:
        """
        Synchronous method to view the balance

        Examples:
            >>> CaptchaControl(api_key="CAI-12345").get_balance()
            ResponseSer(balance=1.0 errorId=False ErrorCode=None errorDescription=None)

        Returns:
            ResponseSer model with full server response

        Notes:
            https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426080/getBalance+retrieve+account+balance
        """
        return self._get_sync_result(
            url_postfix=CaptchaControlEnm.GET_BALANCE.value,
        )

    async def aio_get_balance(self) -> ResponseSer:
        """
        Asynchronous method to view the balance

        Examples:
            >>> await CaptchaControl(api_key="CAI-12345").aio_get_balance()
            ResponseSer(balance=1.0 errorId=False ErrorCode=None errorDescription=None)

        Returns:
            ResponseSer model with full server response

        Notes:
            https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426080/getBalance+retrieve+account+balance
        """
        return await self._get_async_result(
            url_postfix=CaptchaControlEnm.GET_BALANCE.value,
        )
