from .const import REQUEST_URL
from .serializer import RequestCreateTaskSer, RequestGetTaskResultSer
from .context_instr import AIOContextManager, SIOContextManager
from .captcha_instrument import CaptchaInstrument

__all__ = ("CaptchaParams",)


class CaptchaParams(SIOContextManager, AIOContextManager):
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

    def __init__(
        self,
        api_key: str,
        sleep_time: int = 5,
        request_url: str = REQUEST_URL,
        **kwargs,
    ):
        # assign args to validator
        self.create_task_payload = RequestCreateTaskSer(clientKey=api_key)
        # `task` body for task creation payload
        self.task_params = {}
        # prepare `get task result` payload
        self.get_result_params = RequestGetTaskResultSer(clientKey=api_key)
        self.request_url = request_url
        self._captcha_handling_instrument = CaptchaInstrument()

    """
    Async part
    """
