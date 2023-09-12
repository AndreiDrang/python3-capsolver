from typing import Union

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import AntiImpervaTaskEnm
from python3_capsolver.core.serializer import AntiImpervaTaskSer, CaptchaResponseSer


class Imperva(BaseCaptcha):
    """
    The class is used to work with Capsolver Imperva method.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``AntiImpervaTask`` and etc.
        websiteUrl: The website url
        userAgent: Browser userAgent

    Examples:
        >>> Imperva(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type="AntiImpervaTask",
        ...          websiteUrl="https://www.milanuncios.com/",
        ...          userAgent="Mozilla/5.0 (Windows ....",
        ...          proxy="socks5:98.181.137.83:4145",
        ...          utmvc=True,
        ...          reese84=True,
        ...          reeseScriptUrl="https://www.milanuncios.com/librarym.js",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': '90F9EAF...'}
                          )

        >>> Imperva(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=AntiImpervaTaskEnm.AntiImpervaTask,
        ...          websiteUrl="https://www.milanuncios.com/",
        ...          userAgent="Mozilla/5.0 (Windows ....",
        ...          proxy="socks5:98.181.137.83:4145",
        ...          utmvc=True,
        ...          reese84=True,
        ...          reeseScriptUrl="https://www.milanuncios.com/librarym.js",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': '90F9EAF...'}
                          )

        >>> await Imperva(api_key="CAI-BA9650D2B9C2786B21120D512702E010",
        ...                 captcha_type=AntiImpervaTaskEnm.AntiImpervaTask,
        ...                 websiteUrl="https://www.milanuncios.com/",
        ...                 userAgent="Mozilla/5.0 (Windows ....",
        ...                 proxy="socks5:98.181.137.83:4145",
        ...                 utmvc=True,
        ...                 reese84=True,
        ...                 reeseScriptUrl="https://www.milanuncios.com/librarym.js",
        ...         ).aio_captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': '90F9EAF...'}
                          )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://docs.capsolver.com/guide/antibots/imperva.html
    """

    def __init__(
        self,
        captcha_type: Union[AntiImpervaTaskEnm, str],
        websiteUrl: str,
        userAgent: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if captcha_type == AntiImpervaTaskEnm.AntiImpervaTask:
            self.task_params = AntiImpervaTaskSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {AntiImpervaTaskEnm.list_values()}"""
            )

        for key in kwargs:
            self.task_params.update({key: kwargs[key]})

    def captcha_handler(self) -> CaptchaResponseSer:
        """
        Sync solving method

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        return self._processing_captcha(create_params=self.task_params)

    async def aio_captcha_handler(self) -> CaptchaResponseSer:
        """
        Async method for captcha solving

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        return await self._aio_processing_captcha(create_params=self.task_params)
