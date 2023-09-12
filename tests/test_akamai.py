import pytest

from tests.conftest import BaseTest
from python3_capsolver.akamai import Akamai


class TestAkamaiBase(BaseTest):
    AKAMAI_WEB_URL = "https://www.xxxx.com/nMRH2/aYJ/PQ4b/32/0peDlm/b9f5NJcXf7tiYE/OE9CMGI1/Nzsn/bCVKCnA"

    def test_captcha_handler_exist(self):
        assert "captcha_handler" in Akamai.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in Akamai.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            Akamai(
                api_key=self.get_random_string(36),
                captcha_type="test",
            )

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            Akamai(api_key=self.get_random_string(36))
