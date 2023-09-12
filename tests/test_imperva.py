import pytest

from tests.conftest import BaseTest
from python3_capsolver.imperva import Imperva
from python3_capsolver.core.enum import AntiImpervaTaskEnm


class TestImpervaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in Imperva.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in Imperva.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            Imperva(
                api_key=self.get_random_string(36),
                captcha_type="test",
                websiteUrl=self.get_random_string(36),
                userAgent=self.get_random_string(36),
            )

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            Imperva(
                api_key=self.get_random_string(36),
                websiteUrl=self.get_random_string(36),
                userAgent=self.get_random_string(36),
            )

    def test_no_websiteUrl(self):
        with pytest.raises(TypeError):
            Imperva(
                api_key=self.get_random_string(36),
                captcha_type=AntiImpervaTaskEnm.AntiImpervaTask,
                userAgent=self.get_random_string(36),
            )

    def test_no_userAgent(self):
        with pytest.raises(TypeError):
            Imperva(
                api_key=self.get_random_string(36),
                captcha_type=AntiImpervaTaskEnm.AntiImpervaTask,
                websiteUrl=self.get_random_string(36),
            )
