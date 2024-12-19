from typing import Union, Optional

from .core.base import CaptchaParams
from .core.enum import AntiAwsWafTaskTypeEnm


class AwsWaf(CaptchaParams):
    def __init__(
        self,
        api_key: str,
        captcha_type: Union[AntiAwsWafTaskTypeEnm, str],
        websiteURL: str,
        sleep_time: Optional[int] = 10,
        **additional_params,
    ):
        """
        The class is used to work with Capsolver AwsWaf methods.

        Args:
            api_key: Capsolver API key
            captcha_type: Captcha type name, like ``AntiAwsWafTask`` and etc.
            websiteURL: Address of a webpage with AwsWaf
            additional_params: Some additional parameters that will be used in creating the task
                                and will be passed to the payload under ``task`` key.
                                Like ``proxyLogin``, ``proxyPassword`` and etc. - more info in service docs


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

        super().__init__(api_key=api_key, sleep_time=sleep_time)

        if captcha_type in AntiAwsWafTaskTypeEnm.list():
            self.task_params.update(dict(type=captcha_type, websiteURL=websiteURL, **additional_params))
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {AntiAwsWafTaskTypeEnm.list_values()}"""
            )
