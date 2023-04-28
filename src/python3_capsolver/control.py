from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import EndpointPostfixEnm
from python3_capsolver.core.serializer import PostRequestSer, ControlResponseSer


class Control(BaseCaptcha):
    """
    The class is used to work with Capsolver control methods.

    Args:
        api_key: Capsolver API key

    Notes:
        https://docs.capsolver.com/guide/api-getbalance.html
    """

    serializer = PostRequestSer

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

    def get_balance(self) -> ControlResponseSer:
        """
        Synchronous method to view the balance

        Examples:
            >>> Control(api_key="CAI-1324...").get_balance()
            ControlResponseSer(errorId=0 errorCode=None errorDescription=None balance=150.9085)

        Returns:
            ResponseSer model with full server response

        Notes:
            https://docs.capsolver.com/guide/api-getbalance.html
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
            >>> await Control(api_key="CAI-1324...").aio_get_balance()
            ControlResponseSer(errorId=0 errorCode=None errorDescription=None balance=150.9085)

        Returns:
            ResponseSer model with full server response

        Notes:
            https://docs.capsolver.com/guide/api-getbalance.html
        """
        self._prepare_create_task_payload(serializer=self.serializer)
        return ControlResponseSer(
            **await self._aio_create_task(
                url_postfix=EndpointPostfixEnm.GET_BALANCE.value,
            )
        )
