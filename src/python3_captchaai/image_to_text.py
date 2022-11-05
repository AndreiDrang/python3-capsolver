from python3_captchaai.core.base import BaseCaptcha
from python3_captchaai.core.enums import CaptchaTypeEnm
from python3_captchaai.core.serializer import CaptchaResponseSer, RequestCreateTaskSer


class BaseImageToText(BaseCaptcha):
    captcha_type = CaptchaTypeEnm.ImageToTextTask


class ImageToText(BaseImageToText):
    """
    The class is used to work with CaptchaAI control methods.

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/393427/ImageToTextTask+beta+solve+image+captcha
    """

    def captcha_handler(self, body: str, **additional_params) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            body: Base64 encoded content of the image
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under `task` key

        Examples:
            >>> with open('some_image.jpeg', 'rb') as img_file: \
                    img_data = img_file.read()
            >>> body = base64.b64encode(img_data).decode("utf-8")
            >>> ImageToText(api_key="CAI-12345....").captcha_handler(body=body)

            CaptchaResponseSer(errorId=False
                                ErrorCode=None
                                errorDescription=None
                                taskId=None
                                status=<ResponseStatusEnm.Ready: 'ready'>
                                solution={'text': 'captcha solution text'}
                            )

        Returns:
            CaptchaResponseSer model with full server response

        Notes:
            https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426080/getBalance+retrieve+account+balance
        """
        return self._processing_captcha(
            serializer=RequestCreateTaskSer, type=self.captcha_type, body=body, **additional_params
        )

    async def aio_captcha_handler(self, body: str, **additional_params) -> CaptchaResponseSer:
        """
        Asynchronous method for captcha solving

        Args:
            body: Base64 encoded content of the image
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under `task` key

        Examples:
            >>> with open('some_image.jpeg', 'rb') as img_file: \
                    img_data = img_file.read()
            >>> body = base64.b64encode(img_data).decode("utf-8")
            >>> await ImageToText(api_key="CAI-12345....").aio_captcha_handler(body=body)

            CaptchaResponseSer(errorId=False
                                ErrorCode=None
                                errorDescription=None
                                taskId=None
                                status=<ResponseStatusEnm.Ready: 'ready'>
                                solution={'text': 'captcha solution text'}
                            )

        Returns:
            CaptchaResponseSer model with full server response

        Notes:
            https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426080/getBalance+retrieve+account+balance
        """
        return await self._aio_processing_captcha(
            serializer=RequestCreateTaskSer, type=self.captcha_type, body=body, **additional_params
        )
