from typing import Dict, Union, Optional

from python3_capsolver.core.base import BaseCaptcha
from python3_capsolver.core.enum import CloudflareTypeEnm
from python3_capsolver.core.serializer import CaptchaResponseSer, CloudflareTurnstileSer


class Cloudflare(BaseCaptcha):
    """
    The class is used to work with Capsolver Cloudflare methods.

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like ``ReCaptchaV2Task`` and etc.
        websiteURL: Address of a webpage with Google ReCaptcha
        websiteKey: Recaptcha website key. <div class="g-recaptcha" data-sitekey="THAT_ONE"></div>
        metadata: Extra data
        html: You can pass in the entire html source code for the challenge directly.


    Examples:
        >>> Cloudflare(api_key="CAI-1324...",
        ...             captcha_type=CloudflareTypeEnm.AntiCloudflareTask,
        ...             websiteURL="https://bck.websiteurl.com/registry",
        ...             websiteKey='4ac25d',
        ...             proxy="socks5:158.120.100.23:334:user:pass",
        ...             metadata={'type': 'turnstile', 'acton':'login', 'cdata': '0000-1111-2222-3333-example-cdata'}
        ...          ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> Cloudflare(api_key="CAI-1324...",
        ...             captcha_type=CloudflareTypeEnm.AntiCloudflareTask,
        ...             websiteURL="https://bck.websiteurl.com/registry",
        ...             proxy="socks5:158.120.100.23:334:user:pass",
        ...             metadata={'type': 'challenge'}
        ...             html="<your challenge html source code>",
        ...          ).captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

        >>> await Cloudflare(api_key="CAI-1324...",
        ...             captcha_type=CloudflareTypeEnm.AntiCloudflareTask,
        ...             websiteURL="https://bck.websiteurl.com/registry",
        ...             websiteKey='4ac25d',
        ...             proxy="socks5:158.120.100.23:334:user:pass",
        ...             metadata={'type': 'challenge', 'acton':'login', 'cdata': '0000-1111-2222-3333-example-cdata'}
        ...          ).aio_captcha_handler()
        CaptchaResponseSer(errorId=0,
                           errorCode=None,
                           errorDescription=None,
                           taskId='73bdcd28-6c77-4414-8....',
                           status=<ResponseStatusEnm.Ready: 'ready'>,
                           solution={'gRecaptchaResponse': '44795sds...'}
                          )

    Returns:
        CaptchaResponseSer model with full server response

    Notes:
        https://docs.capsolver.com/guide/antibots/cloudflare_turnstile.html
        https://docs.capsolver.com/guide/antibots/cloudflare_challenge.html
    """

    def __init__(
        self,
        captcha_type: Union[CloudflareTypeEnm, str],
        websiteURL: str,
        metadata: Dict[str, str],
        websiteKey: Optional[str] = None,
        html: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if captcha_type in CloudflareTypeEnm.list():
            self.task_params = CloudflareTurnstileSer(**locals()).dict(exclude_none=True)
        else:
            raise ValueError(
                f"""Invalid `captcha_type` parameter set for `{self.__class__.__name__}`,
                available - {CloudflareTypeEnm.list()}"""
            )
        for key in kwargs:
            self.task_params.update({key: kwargs[key]})

    def captcha_handler(self) -> CaptchaResponseSer:
        """
        Sync method for captcha solving

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
