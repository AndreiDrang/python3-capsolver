from typing import Union

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import AntiAkamaiTaskEnm, EndpointPostfixEnm
from python3_capsolver.core.serializer import (
    PostRequestSer,
    CaptchaResponseSer,
    AntiAkamaiBMPTaskSer,
    AntiAkamaiWebTaskSer,
)


class Akamai(BaseCaptcha):
    """
    The class is used to work with Capsolver AntiAkamai methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``AntiAkamaiBMPTask`` and etc.
        packageName: Package name of AkamaiBMP mobile APP
        version: AKAMAI BMP Version number, default is: 3.2.6 , max support 3.3.1

    Examples:
        >>> Akamai(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type="AntiAkamaiBMPTask",
        ...          packageName="de.zalando.iphone",
        ...          country="US",
        ...          deviceId="90F9EAF5-D6E5-4E30-BC8B-B7780AD02600",
        ...          deviceName="iPhone14,2/16.0.2",
        ...          count=10,
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'deviceId': '90F9EAF...'}
                          )

        >>> Akamai(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type="AntiAkamaiWebTask",
        ...          url="https://www.xxxx.com/nMRH2/aYJ/PQ4b/32/0peDlm/b9f5NJcXf7tiYE/OE9CMGI1/Nzsn/bCVKCnA",
        ...          abck="14164862507BD4......",
        ...          bmsz="4E3C....33",
        ...          userAgent="Mozilla/5.0 (Wi....",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'sensorData': '2;3159346;4338233...'}
                          )

        >>> Akamai(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=AntiAkamaiTaskEnm.AntiAkamaiBMPTask,
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'deviceId': '6DKFOD0...'}
                          )

        >>> Akamai(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=AntiAkamaiTaskEnm.AntiAkamaiWebTask,
        ...          url="https://www.xxxx.com/nMRH2/aYJ/PQ4b/32/0peDlm/b9f5NJcXf7tiYE/OE9CMGI1/Nzsn/bCVKCnA",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'sensorData': '2;3159346;4338233...'}
                          )

        >>> Akamai(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=AntiAkamaiTaskEnm.AntiAkamaiBMPTask,
        ...          **{
        ...              "version": "3.2.6",
        ...              "deviceId": "90F9EAF5-D6E5-4E30-BC8B-B7780AD02600",
        ...              "deviceName": "iPhone14,2/16.0.2",
        ...              "count": 10,
        ...            },
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId="87f149f4-1c....",
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'deviceId': '90F9EAF...'}
                          )

        >>> await Akamai(api_key="CAI-BA9650D2B9C2786B21120D512702E010",
        ...                 captcha_type="AntiAkamaiBMPTask",
        ...                 packageName="de.zalando.iphone",
        ...                 country="US",
        ...                 deviceId="90F9EAF5-D6E5-4E30-BC8B-B7780AD02600",
        ...                 deviceName="iPhone14,2/16.0.2",
        ...                 count=10,
        ...         ).aio_captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'deviceId': '90F9EAF...'}
                          )

        >>> await Akamai(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=AntiAkamaiTaskEnm.AntiAkamaiWebTask,
        ...          url="https://www.xxxx.com/nMRH2/aYJ/PQ4b/32/0peDlm/b9f5NJcXf7tiYE/OE9CMGI1/Nzsn/bCVKCnA",
        ...         ).aio_captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'sensorData': '2;3159346;4338233...'}
                          )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://docs.capsolver.com/guide/antibots/akamaibmp.html
        https://docs.capsolver.com/guide/antibots/akamaiweb.html
    """

    def __init__(
        self,
        captcha_type: Union[AntiAkamaiTaskEnm, str],
        packageName: str = "de.zalando.iphone",
        version: str = "3.2.6",
        country: str = "US",
        url: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.__serializer = PostRequestSer
        self.__url_postfix = None

        if captcha_type == AntiAkamaiTaskEnm.AntiAkamaiBMPTask:
            self.task_params = AntiAkamaiBMPTaskSer(**locals()).dict()
            self.__url_postfix = EndpointPostfixEnm.AKAMAI_BMP_INVOKE.value
        elif captcha_type == AntiAkamaiTaskEnm.AntiAkamaiWebTask:
            self.task_params = AntiAkamaiWebTaskSer(**locals()).dict()
            self.__url_postfix = EndpointPostfixEnm.AKAMAI_WEB_INVOKE.value
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {AntiAkamaiTaskEnm.list_values()}"""
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
        self._prepare_create_task_payload(serializer=self.__serializer, create_params=self.task_params)
        return CaptchaResponseSer(
            **self._create_task(
                url_postfix=self.__url_postfix,
            )
        )

    async def aio_captcha_handler(self) -> CaptchaResponseSer:
        """
        Async method for captcha solving

        Returns:
            CaptchaResponseSer model with full service response

        Notes:
            Check class docstring for more info
        """
        self._prepare_create_task_payload(serializer=self.__serializer, create_params=self.task_params)
        return CaptchaResponseSer(
            **await self._aio_create_task(
                url_postfix=self.__url_postfix,
            )
        )
