import pytest

from tests.conftest import BaseTest
from python3_capsolver.imperva import Imperva
from python3_capsolver.core.enum import AntiImpervaTaskEnm
from python3_capsolver.core.serializer import CaptchaResponseSer


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


class TestAntiImpervaTaskBase(BaseTest):
    def test_instance(self):
        instance = Imperva(
            api_key=self.API_KEY,
            captcha_type=AntiImpervaTaskEnm.AntiImpervaTask,
            websiteUrl="https://www.milanuncios.com/",
            userAgent=self.get_random_string(36),
            proxy=self.get_random_string(36),
            utmvc=True,
            reese84=True,
            reeseScriptUrl="https://www.milanuncios.com/librarym.js",
        )

    def test_solve(self):
        instance = Imperva(
            api_key=self.API_KEY,
            captcha_type=AntiImpervaTaskEnm.AntiImpervaTask,
            websiteUrl="https://www.milanuncios.com/",
            userAgent=self.get_random_string(36),
            proxy="socks5:98.181.137.83:4145",
            utmvc=True,
            reese84=True,
            reeseScriptUrl="https://www.milanuncios.com/librarym.js",
        )
        result = instance.captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_PROXY_CONNECT_REFUSED"

    async def test_aio_solve(self):
        instance = Imperva(
            api_key=self.API_KEY,
            captcha_type=AntiImpervaTaskEnm.AntiImpervaTask,
            websiteUrl="https://www.milanuncios.com/",
            userAgent=self.get_random_string(36),
            proxy="socks5:98.181.137.83:4145",
            utmvc=True,
            reese84=True,
            reeseScriptUrl="https://www.milanuncios.com/librarym.js",
        )
        result = await instance.aio_captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_PROXY_CONNECT_REFUSED"
