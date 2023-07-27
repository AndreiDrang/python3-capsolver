from typing import Union

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import ImageToTextTaskTypeEnm
from python3_capsolver.core.serializer import TaskSer, CaptchaResponseSer


class ImageToText(BaseCaptcha):
    """
    The class is used to work with Capsolver Image captcha solving methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``ImageToTextTask`` and etc.

    Examples:
        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> ImageToText(api_key="CAI-12345....").captcha_handler(body=body)
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'confidence': 0.9585, 'text': 'gcphjd'}
                          )

        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> ImageToText(api_key="CAI-12345....",
        ...             module='queueit'
        ...            ).captcha_handler(body=body)
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'confidence': 0.9585, 'text': 'zzzzz'}
                          )

        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> ImageToText(api_key="CAI-12345....",
        ...             module='dell',
        ...             score=0.98,
        ...             case=True,
        ...            ).captcha_handler(body=body)
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'confidence': 0.9585, 'text': 'gcphjd'}
                          )

        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> with ImageToText(api_key="CAI-12345....") as image_to_text_inst:
        ...    image_to_text_inst.captcha_handler(body=body)
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'confidence': 0.9585, 'text': 'gcphjd'}
                          )

        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> await ImageToText(api_key="CAI-12345....").aio_captcha_handler(body=body)
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'confidence': 0.9585, 'text': 'gcphjd'}
                          )

        >>> with open('some_image.jpeg', 'rb') as img_file:
        ...    img_data = img_file.read()
        >>> body = base64.b64encode(img_data).decode("utf-8")
        >>> with ImageToText(api_key="CAI-12345....") as image_to_text_inst:
        ...    await image_to_text_inst.aio_captcha_handler(body=body)
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'confidence': 0.9585, 'text': 'gcphjd'}
                          )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://docs.capsolver.com/guide/recognition/ImageToTextTask.html
    """

    def __init__(
        self,
        captcha_type: Union[ImageToTextTaskTypeEnm, str] = ImageToTextTaskTypeEnm.ImageToTextTask,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if captcha_type in ImageToTextTaskTypeEnm.list():
            self.task_params = TaskSer(**locals()).dict(exclude_none=True)
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {ImageToTextTaskTypeEnm.list()}"""
            )
        for key in kwargs:
            self.task_params.update({key: kwargs[key]})

    def captcha_handler(self, body: str) -> CaptchaResponseSer:
        """
        Synchronous method for captcha solving

        Args:
            body: Base64 encoded content of the image, decoded into str

        Returns:
            CaptchaResponseSer model with full server response

        Notes:
            Check class docstring for more info
        """
        self.task_params.update({"body": body})
        return self._processing_captcha(create_params=self.task_params)

    async def aio_captcha_handler(self, body: str) -> CaptchaResponseSer:
        """
        Asynchronous method for captcha solving

        Args:
            body: Base64 encoded content of the image, decoded into str

        Returns:
            CaptchaResponseSer model with full server response

        Notes:
            Check class docstring for more info
        """
        self.task_params.update({"body": body})
        return await self._aio_processing_captcha(create_params=self.task_params)
