import pytest

from tests.conftest import BaseTest
from python3_capsolver.akamai import Akamai
from python3_capsolver.core.enum import AntiAkamaiTaskEnm
from python3_capsolver.core.serializer import CaptchaResponseSer


class TestAkamaiBase(BaseTest):
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


class TestAkamaiBMPBase(BaseTest):
    captcha_type = AntiAkamaiTaskEnm.AntiAkamaiBMPTask

    def test_solve(self):
        instance = Akamai(api_key=self.API_KEY, captcha_type=self.captcha_type)
        result = instance.captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 0
        assert result.errorCode is None
        assert result.errorDescription is None
        assert result.solution is not None

    async def test_aio_solve(self):
        instance = Akamai(api_key=self.API_KEY, captcha_type=self.captcha_type)
        result = await instance.aio_captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 0
        assert result.errorCode is None
        assert result.errorDescription is None
        assert result.solution is not None

    def test_solve_context(self):
        with Akamai(api_key=self.API_KEY, captcha_type=self.captcha_type) as instance:
            result = instance.captcha_handler()
            assert isinstance(result, CaptchaResponseSer)
            assert result.errorId == 0
            assert result.errorCode is None
            assert result.errorDescription is None
            assert result.solution is not None

    async def test_aio_solve_context(self):
        with Akamai(api_key=self.API_KEY, captcha_type=self.captcha_type) as instance:
            result = await instance.aio_captcha_handler()
            assert isinstance(result, CaptchaResponseSer)
            assert result.errorId == 0
            assert result.errorCode is None
            assert result.errorDescription is None
            assert result.solution is not None


class TestAkamaiWebBase(BaseTest):
    captcha_type = AntiAkamaiTaskEnm.AntiAkamaiWebTask
    akamai_web_url = "https://www.xxxx.com/nMRH2/aYJ/PQ4b/32/0peDlm/b9f5NJcXf7tiYE/OE9CMGI1/Nzsn/bCVKCnA"

    def test_solve(self):
        instance = Akamai(api_key=self.API_KEY, captcha_type=self.captcha_type, url=self.akamai_web_url)
        result = instance.captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 0
        assert result.errorCode is None
        assert result.errorDescription is None
        assert result.solution is not None

    async def test_aio_solve(self):
        instance = Akamai(api_key=self.API_KEY, captcha_type=self.captcha_type, url=self.akamai_web_url)
        result = await instance.aio_captcha_handler()
        assert isinstance(result, CaptchaResponseSer)
        assert result.errorId == 0
        assert result.errorCode is None
        assert result.errorDescription is None
        assert result.solution is not None

    def test_solve_context(self):
        with Akamai(api_key=self.API_KEY, captcha_type=self.captcha_type, url=self.akamai_web_url) as instance:
            result = instance.captcha_handler()
            assert isinstance(result, CaptchaResponseSer)
            assert result.errorId == 0
            assert result.errorCode is None
            assert result.errorDescription is None
            assert result.solution is not None

    async def test_aio_solve_context(self):
        with Akamai(api_key=self.API_KEY, captcha_type=self.captcha_type, url=self.akamai_web_url) as instance:
            result = await instance.aio_captcha_handler()
            assert isinstance(result, CaptchaResponseSer)
            assert result.errorId == 0
            assert result.errorCode is None
            assert result.errorDescription is None
            assert result.solution is not None
