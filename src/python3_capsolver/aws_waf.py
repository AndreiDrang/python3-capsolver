from typing import Union

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import AntiAwsWafTaskTypeEnm
from python3_capsolver.core.serializer import CaptchaResponseSer, WebsiteDataOptionsSer


class AwsWaf(BaseCaptcha):
    """
    The class is used to work with Capsolver AwsWaf methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``AntiAwsWafTask`` and etc.
        websiteURL: Address of a webpage with AwsWaf

    Examples:
        >>> AwsWaf(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type='AntiAwsWafTaskProxyLess',
        ...          websiteURL="https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'cookie': '44795sds...'}
                          )

        >>> AwsWaf(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=AntiAwsWafTaskTypeEnm.AntiAwsWafTaskProxyLess,
        ...          websiteURL="https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest",
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'cookie': '44795sds...'}
                          )

        >>> AwsWaf(api_key="CAI-BA9XXXXXXXXXXXXX2702E010",
        ...          captcha_type=AntiAwsWafTaskTypeEnm.AntiAwsWafTask,
        ...          websiteURL="https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest",
        ...          proxy="socks5:192.191.100.10:4780:user:pwd",
        ...          awsKey="some key"
        ...         ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId="87f149f4-1c....",
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'cookie': '44795sds...'}
                          )

        >>> await AwsWaf(api_key="CAI-BA9650D2B9C2786B21120D512702E010",
        ...          captcha_type=AntiAwsWafTaskTypeEnm.AntiAwsWafTaskProxyLess,
        ...          websiteURL="https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest",
        ...         ).aio_captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'cookie': '44795sds...'}
                          )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://docs.capsolver.com/guide/captcha/awsWaf.html
    """

    def __init__(self, captcha_type: Union[AntiAwsWafTaskTypeEnm, str], websiteURL: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if captcha_type in AntiAwsWafTaskTypeEnm.list():
            self.task_params = WebsiteDataOptionsSer(**locals()).dict()
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {AntiAwsWafTaskTypeEnm.list_values()}"""
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
