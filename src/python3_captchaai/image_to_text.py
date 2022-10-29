from src.python3_captchaai.core.base import BaseCaptcha
from src.python3_captchaai.core.enums import CaptchaTypeEnm
from src.python3_captchaai.core.serializer import ImageToTextTask, CaptchaResponseSer


class BaseControl(BaseCaptcha):
    pass


class ImageToText(BaseControl):
    """
    The class is used to work with CaptchaAI control methods.

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/393427/ImageToTextTask+beta+solve+image+captcha
    """

    def captcha_handler(self, body, **additional_params) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Examples:
            >>> ImageToText(api_key="CAI-12345").captcha_handler()
            CaptchaResponseSer(balance=1.0 errorId=False ErrorCode=None errorDescription=None)

        Returns:
            ResponseSer model with full server response

        Notes:
            https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426080/getBalance+retrieve+account+balance
        """
        return self._processing_captcha(
            serializer=ImageToTextTask, type=CaptchaTypeEnm.ImageToTextTask, body=body, **additional_params
        )
