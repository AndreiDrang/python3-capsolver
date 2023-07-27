from typing import Union

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import AntiCyberSiAraTaskTypeEnm
from python3_capsolver.core.serializer import CyberSiAraSer, CaptchaResponseSer


class CyberSiARA(BaseCaptcha):
    """
    The class is used to work with Capsolver CyberSiARA methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``AntiCyberSiAraTask`` and etc.
        websiteURL: Address of a webpage with CyberSiARA
        SlideMasterUrlId: You can get MasterUrlId param form `api/CyberSiara/GetCyberSiara` endpoint request
        UserAgent: Browser userAgent, you need submit your userAgent

    Examples:
        >>> CyberSiARA(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type='AntiCyberSiAraTaskProxyLess',
        ...          websiteURL="https://www.cybersiara.com/book-a-demo",
        ...          UserAgent="Mozilla/5.0 ....",
        ...          SlideMasterUrlId="OXR2LVNvCuXykkZbB8KZIfh162sNT8S2",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': '44795sds...'}
                          )

        >>> CyberSiARA(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=AntiCyberSiAraTaskTypeEnm.AntiCyberSiAraTaskProxyLess,
        ...          websiteURL="https://www.cybersiara.com/book-a-demo",
        ...          UserAgent="Mozilla/5.0 ....",
        ...          SlideMasterUrlId="OXR2LVNvCuXykkZbB8KZIfh162sNT8S2",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': '44795sds...'}
                          )

        >>> CyberSiARA(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=AntiCyberSiAraTaskTypeEnm.AntiCyberSiAraTask,
        ...          websiteURL="https://www.cybersiara.com/book-a-demo",
        ...          UserAgent="Mozilla/5.0 ....",
        ...          SlideMasterUrlId="OXR2LVNvCuXykkZbB8KZIfh162sNT8S2",
        ...          proxy="socks5:192.191.100.10:4780:user:pwd",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId="87f149f4-1c....",
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': '44795sds...'}
                          )

        >>> await CyberSiARA(api_key="CAI-BA9650D2B9C2786B21120D512702E010",
        ...          captcha_type=AntiCyberSiAraTaskTypeEnm.AntiCyberSiAraTaskProxyLess,
        ...          websiteURL="https://www.cybersiara.com/book-a-demo",
        ...          UserAgent="Mozilla/5.0 ....",
        ...          SlideMasterUrlId="OXR2LVNvCuXykkZbB8KZIfh162sNT8S2",
        ...         ).aio_captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'token': '44795sds...'}
                          )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://docs.capsolver.com/guide/captcha/CyberSiara.html
    """

    def __init__(
        self,
        captcha_type: Union[AntiCyberSiAraTaskTypeEnm, str],
        websiteURL: str,
        SlideMasterUrlId: str,
        UserAgent: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if captcha_type in AntiCyberSiAraTaskTypeEnm.list():
            self.task_params = CyberSiAraSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {AntiCyberSiAraTaskTypeEnm.list_values()}"""
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
