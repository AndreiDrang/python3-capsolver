from .core.base import CaptchaParams
from .core.enum import CaptchaTypeEnm
from .core.const import GET_BALANCE_POSTFIX
from .core.aio_captcha_instrument import AIOCaptchaInstrument
from .core.sio_captcha_instrument import SIOCaptchaInstrument

__all__ = ("Control",)


class Control(CaptchaParams):
    """
    The class is used to work with Capsolver control methods.

    Args:
        api_key: Capsolver API key

    Notes:
        https://docs.capsolver.com/en/guide/api-getbalance/
    """

    def __init__(
        self,
        api_key: str,
    ):
        super().__init__(api_key=api_key, captcha_type=CaptchaTypeEnm.Control)

    def get_balance(self) -> dict:
        """
        Synchronous method to view the balance

        Examples:
            >>> from python3_capsolver.control import Control
            >>> Control(api_key="CAI-1324...").get_balance()
            {'balance': 48.6361, 'errorId': 0, 'packages': []}

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        self._captcha_handling_instrument = SIOCaptchaInstrument(captcha_params=self)
        return self._captcha_handling_instrument.send_post_request(
            session=self._captcha_handling_instrument.session,
            url_postfix=GET_BALANCE_POSTFIX,
            payload={"clientKey": self.create_task_payload.clientKey},
        )

    async def aio_get_balance(self) -> dict:
        """
        Asynchronous method to view the balance

        Examples:
        >>> import asyncio
        >>> from python3_capsolver.control import Control
        >>> asyncio.run(Control(api_key="CAI-1324...").aio_get_balance())
        {'balance': 48.6361, 'errorId': 0, 'packages': []}

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=GET_BALANCE_POSTFIX,
            payload={"clientKey": self.create_task_payload.clientKey},
        )
