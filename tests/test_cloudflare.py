import pytest

from tests.conftest import BaseTest
from python3_capsolver.core.enum import CloudflareTypeEnm
from python3_capsolver.cloudflare import Cloudflare
from python3_capsolver.core.serializer import CaptchaResponseSer


class TestCloudflareBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in Cloudflare.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in Cloudflare.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            Cloudflare(
                api_key=self.get_random_string(36),
                captcha_type="test",
                websiteURL=self.get_random_string(36),
            )

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            Cloudflare(
                api_key=self.get_random_string(36),
                websiteURL=self.get_random_string(36),
            )

    def test_no_websiteURL(self):
        with pytest.raises(TypeError):
            Cloudflare(
                api_key=self.get_random_string(36),
                captcha_type=CloudflareTypeEnm.AntiCloudflareTask,
                validateId=self.get_random_string(36),
            )


class TestAntiCloudflareTaskBase(BaseTest):
    def test_instance(self):
        instance = Cloudflare(
            api_key=self.API_KEY,
            captcha_type=CloudflareTypeEnm.AntiCloudflareTask,
            websiteURL="https://bck.websiteurl.com/registry",
            proxy="socks5:158.120.100.23:334:user:pass",
        )

    def test_solve(self):
        instance = Cloudflare(
            api_key=self.API_KEY,
            captcha_type=CloudflareTypeEnm.AntiCloudflareTask,
            websiteURL="https://bck.websiteurl.com/registry",
            websiteKey="0x4AAAAAAABS7vwvV6VFfMcD",
            proxy="socks5:158.120.100.23:334:user:pass",
        )
        result = instance.captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_PROXY_CONNECT_REFUSED"

    async def test_aio_solve(self):
        instance = Cloudflare(
            api_key=self.API_KEY,
            captcha_type=CloudflareTypeEnm.AntiCloudflareTask,
            websiteURL="https://bck.websiteurl.com/registry",
            websiteKey="0x4AAAAAAABS7vwvV6VFfMcD",
            proxy="socks5:158.120.100.23:334:user:pass",
        )
        result = await instance.aio_captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_PROXY_CONNECT_REFUSED"
