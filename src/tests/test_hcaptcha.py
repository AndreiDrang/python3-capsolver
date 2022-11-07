import pytest
from pydantic import ValidationError

from src.tests.conftest import BaseTest
from python3_captchaai.hcaptcha import HCaptcha
from python3_captchaai.core.enum import ProxyType, CaptchaTypeEnm

HCAPTCHA_KEY = "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2"
PAGE_URL = "https://accounts.hcaptcha.com/demo"


class TestHCaptchaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in HCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in HCaptcha.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            HCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.Control,
                websiteURL=self.get_random_string(5),
                websiteKey=self.get_random_string(5),
            )

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            HCaptcha(
                api_key=self.get_random_string(36),
                websiteURL=self.get_random_string(5),
                websiteKey=self.get_random_string(5),
            )


class TestHCaptchaProxyless(BaseTest):
    hcaptcha_key = HCAPTCHA_KEY
    pageurl = PAGE_URL

    captcha_type = CaptchaTypeEnm.HCaptchaTaskProxyless
    """
    Success tests
    """

    def test_params(self):
        HCaptcha(
            api_key=self.API_KEY, captcha_type=self.captcha_type, websiteURL=self.pageurl, websiteKey=self.hcaptcha_key
        )

    def test_params_context(self):
        with HCaptcha(
            api_key=self.API_KEY, captcha_type=self.captcha_type, websiteURL=self.pageurl, websiteKey=self.hcaptcha_key
        ) as instance:
            pass

    # TODO start use it, temporary Captcha not solving
    """    def test_solve(self):
            resp = HCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
            ).captcha_handler()
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status == ResponseStatusEnm.Ready
            assert resp.errorId is False
            assert resp.errorCode is None
            assert resp.errorDescription is None
            assert resp.solution is not None
    
        def test_solve_context(self):
            with HCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
            ) as instance:
                resp = instance.captcha_handler()
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status == ResponseStatusEnm.Ready
            assert resp.errorId is False
            assert resp.errorCode is None
            assert resp.errorDescription is None
            assert resp.solution is not None
    
        async def test_aio_solve(self):
            resp = await HCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
            ).aio_captcha_handler()
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status == ResponseStatusEnm.Ready
            assert resp.errorId is False
            assert resp.errorCode is None
            assert resp.errorDescription is None
            assert resp.solution is not None
    
        async def test_aio_solve_context(self):
            async with HCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
            ) as instance:
                resp = await instance.aio_captcha_handler()
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status == ResponseStatusEnm.Ready
            assert resp.errorId is False
            assert resp.errorCode is None
            assert resp.errorDescription is None
            assert resp.solution is not None
    """
    """
    Failed tests
    """

    def test_no_website_key(self):
        with pytest.raises(ValidationError):
            HCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteURL=self.pageurl)

    def test_no_website_url(self):
        with pytest.raises(ValidationError):
            HCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteKey=self.hcaptcha_key)

    async def test_aio_api_key_err(self):
        with pytest.raises(Exception):
            await HCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
            ).aio_captcha_handler()

    def test_api_key_err(self):
        with pytest.raises(Exception):
            HCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
            ).captcha_handler()


class TestHCaptcha(BaseTest):
    hcaptcha_key = HCAPTCHA_KEY
    pageurl = PAGE_URL
    proxyAddress = "0.0.0.0"
    proxyPort = 9999

    captcha_type = CaptchaTypeEnm.HCaptchaTask

    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_params(self, proxy_type: str):
        HCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.hcaptcha_key,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_params_context(self, proxy_type: str):
        with HCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.hcaptcha_key,
            proxyAddress=self.proxyAddress,
            proxyType=proxy_type,
            proxyPort=self.proxyPort,
        ) as instance:
            pass

    """
    Failed tests
    """

    def test_no_website_key(self):
        with pytest.raises(ValidationError):
            HCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteURL=self.pageurl)

    def test_no_website_url(self):
        with pytest.raises(ValidationError):
            HCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteKey=self.hcaptcha_key)

    def test_no_proxy_type(self):
        with pytest.raises(ValidationError):
            HCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
                proxyAddress=self.proxyAddress,
                proxyPort=self.proxyPort,
            )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxy_address(self, proxy_type: str):
        with pytest.raises(ValidationError):
            HCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
                proxyType=proxy_type,
                proxyPort=self.proxyPort,
            )

    @pytest.mark.parametrize("proxy_type", ProxyType.list_values())
    def test_no_proxy_port(self, proxy_type):
        with pytest.raises(ValidationError):
            HCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
                proxyAddress=self.proxyAddress,
                proxyType=proxy_type,
            )

    async def test_aio_api_key_err(self):
        with pytest.raises(Exception):
            await HCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.googlekey,
            ).aio_captcha_handler()

    def test_api_key_err(self):
        with pytest.raises(Exception):
            HCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=self.pageurl,
                websiteKey=self.hcaptcha_key,
            ).captcha_handler()


class TestHCaptchaClassification(BaseTest):
    hcaptcha_key = HCAPTCHA_KEY
    pageurl = PAGE_URL
    proxyAddress = "0.0.0.0"
    proxyPort = 9999

    captcha_type = CaptchaTypeEnm.HCaptchaClassification
    questions = ["2+2=?", "our planet name"]

    """
    Success tests
    """

    @pytest.mark.parametrize("question", questions)
    def test_params(self, question: str):
        HCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            queries=[
                self.get_random_string(5),
                self.get_random_string(5),
            ],
            question=question,
        )

    @pytest.mark.parametrize("question", questions)
    def test_params_context(self, question: str):
        with HCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            queries=[
                self.get_random_string(5),
                self.get_random_string(5),
            ],
            question=question,
        ) as instance:
            pass

    @pytest.mark.parametrize("question", questions)
    async def test_aio_params_context(self, question: str):
        async with HCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            queries=[
                self.get_random_string(5),
                self.get_random_string(5),
            ],
            question=question,
        ) as instance:
            pass

    """
    Failed tests
    """

    @pytest.mark.parametrize("question", questions)
    def test_no_queries(self, question: str):
        with pytest.raises(ValidationError):
            HCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type, question=question)

    def test_no_question(self):
        with pytest.raises(ValidationError):
            HCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                queries=[
                    self.get_random_string(5),
                    self.get_random_string(5),
                ],
            )

    @pytest.mark.parametrize("question", questions)
    async def test_aio_api_key_err(self, question: str):
        with pytest.raises(Exception):
            await HCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                queries=[
                    self.get_random_string(5),
                    self.get_random_string(5),
                ],
                question=question,
            ).aio_captcha_handler()

    @pytest.mark.parametrize("question", questions)
    def test_api_key_err(self, question: str):
        with pytest.raises(Exception):
            HCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                queries=[
                    self.get_random_string(5),
                    self.get_random_string(5),
                ],
                question=question,
            ).captcha_handler()
