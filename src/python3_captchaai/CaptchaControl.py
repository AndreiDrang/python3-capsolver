from .base import BaseCaptcha


class BaseCaptchaControl(BaseCaptcha):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class CaptchaControl(BaseCaptchaControl):
    """
    The class is used to work with CaptchaAI control methods.
    Solve description:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426042/API+Methods
    """
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

    def get_balance(self) -> dict:
        """
        Retrieve an account balance.

        Returns:

        """
        return self._get_sync_result(
            get_payload=self.__get_payload,
            sleep_time=self.__params.sleep_time,
            url_response=self.__params.url_response,
            result=self.__result,
        )


class aioCaptchaControl(BaseCaptchaControl):
    """
    The class is used to async work with RuCaptcha control methods.
    Solve description:
        https://rucaptcha.com/api-rucaptcha#manage_pingback
        https://rucaptcha.com/api-rucaptcha#complain
        https://rucaptcha.com/api-rucaptcha#additional
    """

    async def domain_control(self, addr: str) -> dict:
        """
        Callback domains control
            https://rucaptcha.com/api-rucaptcha#manage_pingback
        :param addr: Your URL to send a response.
        :return: Dict with result
        """
        self.get_payload.update({"addr": addr})
        return await self.get_async_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
        )

    async def report(self, id: str) -> dict:
        """
        Callback results report
            https://rucaptcha.com/api-rucaptcha#complain
        :param id: Captcha solving task ID
        :return: Dict with result
        """
        self.get_payload.update({"addr": id})
        return await self.get_async_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
        )

    async def additional_methods(self, **kwargs) -> dict:
        """
        Callback results report
            https://rucaptcha.com/api-rucaptcha#additional
        :param kwargs: Additional params for method
        :return: Dict with result
        """
        # If more parameters are passed, add them to get_payload
        if kwargs:
            for key in kwargs:
                self.get_payload.update({key: kwargs[key]})
        return await self.get_async_result(
            get_payload=self.get_payload,
            sleep_time=self.params.sleep_time,
            url_response=self.params.url_response,
            result=self.result,
        )


'''
# Async WebSocket method
class sockCaptchaControl(WebSocketRuCaptcha):
    def __init__(self, rucaptcha_key: str, allSessions: bool = None, suppressSuccess: bool = None):
        """
        Method setup WebSocket connection data
        Params description check in parent class
        """
        super().__init__(allSessions, suppressSuccess)
        self.rucaptcha_key = rucaptcha_key

    async def get_balance(self) -> dict:
        """
        The asynchronous WebSocket method return account balance.
        More info - https://wsrucaptcha.docs.apiary.io/#reference/4
        :return: Server response dict
        """
        balance_payload = ControlCaptchaSocketSer(
            **{
                "method": "balance",
            }
        )
        return await self.send_request(balance_payload.json(exclude_none=True))

    async def report(self, success: bool, captchaId: int) -> dict:
        """
        The asynchronous WebSocket method send captcha solving reports (success or fail).
        More info - https://wsrucaptcha.docs.apiary.io/#reference/2
        :param success: Is captcha solved success?
        :param captchaId: Captcha task unique id. For example - 5034284222
        :return: Server response dict
        """
        report_payload = ControlCaptchaSocketSer(
            **{
                "method": "report",
                "success": success,
                "captchaId": captchaId,
            }
        )

        return await self.send_request(report_payload.json(exclude_none=True))
'''
