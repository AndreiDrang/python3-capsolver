import pytest

from tests.conftest import BaseTest
from python3_capsolver.core.enum import CloudflareTypeEnm
from python3_capsolver.cloudflare import Cloudflare


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
