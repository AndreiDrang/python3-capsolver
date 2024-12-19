from python3_capsolver.core.serializer import PostRequestSer

from .core.base import CaptchaParams
from .core.const import GET_BALANCE_POSTFIX
from .core.aio_captcha_instrument import AIOCaptchaInstrument
from .core.sio_captcha_instrument import SIOCaptchaInstrument


class Control(CaptchaParams):

    serializer = PostRequestSer

    def __init__(
        self,
        api_key: str,
        *args,
        **kwargs,
    ):
        """
        The class is used to work with Capsolver control methods.

        Args:
            api_key: Capsolver API key

        Notes:
            https://docs.capsolver.com/guide/api-getbalance.html
        """
        super().__init__(api_key=api_key, *args, **kwargs)

    def get_balance(self) -> dict:
        """
        Synchronous method to view the balance

        Examples:
            >>> Control(api_key="CAI-1324...").get_balance()
            ControlResponseSer(errorId=0 errorCode=None errorDescription=None balance=150.9085)

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
            >>> await Control(api_key="CAI-1324...").aio_get_balance()
            ControlResponseSer(errorId=0 errorCode=None errorDescription=None balance=150.9085)

        Returns:
            Dict with full server response

        Notes:
            Check class docstring for more info
        """
        return await AIOCaptchaInstrument.send_post_request(
            url_postfix=GET_BALANCE_POSTFIX,
            payload={"clientKey": self.create_task_payload.clientKey},
        )
