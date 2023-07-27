import base64

import pytest

from tests.conftest import BaseTest
from python3_capsolver.hcaptcha import HCaptcha, HCaptchaClassification
from python3_capsolver.core.enum import HCaptchaTypeEnm, HCaptchaClassificationTypeEnm

HCAPTCHA_KEY = "3ceb8624-1970-4e6b-91d5-70317b70b651"
PAGE_URL = "https://accounts.hcaptcha.com/demo"

with open("tests/files/hcap_select.png", "rb") as img_file:
    img_data = img_file.read()


class TestHCaptchaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in HCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in HCaptcha.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            HCaptcha(
                api_key=self.get_random_string(36),
                captcha_type="test",
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

    captcha_type = HCaptchaTypeEnm.HCaptchaTaskProxyless
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
            assert resp.errorId == 0
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
            assert resp.errorId == 0
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
            assert resp.errorId == 0
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
            assert resp.errorId == 0
            assert resp.errorCode is None
            assert resp.errorDescription is None
            assert resp.solution is not None
    """
    """
    Failed tests
    """

    def test_no_website_key(self):
        with pytest.raises(TypeError):
            HCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteURL=self.pageurl)

    def test_no_website_url(self):
        with pytest.raises(TypeError):
            HCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteKey=self.hcaptcha_key)

    async def test_aio_api_key_err(self):
        result = await HCaptcha(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.hcaptcha_key,
        ).aio_captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution

    def test_api_key_err(self):
        result = HCaptcha(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=self.pageurl,
            websiteKey=self.hcaptcha_key,
        ).captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution


class TestHCaptcha(BaseTest):
    hcaptcha_key = HCAPTCHA_KEY
    pageurl = PAGE_URL

    captcha_type = HCaptchaTypeEnm.HCaptchaTask

    """
    Success tests
    """

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
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

    @pytest.mark.parametrize("proxy_type", BaseTest.proxyTypes)
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
        with pytest.raises(TypeError):
            HCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteURL=self.pageurl)

    def test_no_website_url(self):
        with pytest.raises(TypeError):
            HCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type, websiteKey=self.hcaptcha_key)


class TestHCaptchaClassification(BaseTest):
    hcaptcha_key = HCAPTCHA_KEY
    pageurl = PAGE_URL

    image_body = base64.b64encode(img_data).decode("utf-8")

    captcha_type = HCaptchaClassificationTypeEnm.HCaptchaClassification
    question = "Please click each image containing a chair"

    """
    Success tests
    """

    def test_params(self):
        HCaptchaClassification(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            queries=[self.image_body],
            question=self.question,
        )

    def test_params_context(self):
        with HCaptchaClassification(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            queries=[self.image_body],
            question=self.question,
        ) as instance:
            pass

    async def test_aio_params_context(self):
        async with HCaptchaClassification(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            queries=[self.image_body],
            question=self.question,
        ) as instance:
            pass

    """
    Failed tests
    """

    def test_no_queries(self):
        with pytest.raises(TypeError):
            HCaptchaClassification(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                question=self.question,
            )

    def test_no_question(self):
        with pytest.raises(TypeError):
            HCaptchaClassification(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                queries=[self.image_body],
            )


"""
    async def test_aio_api_key_err(self):
        result = await HCaptchaClassification(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            queries=[self.image_body],
            question=self.question,
        ).aio_captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution

    def test_api_key_err(self):
        result = HCaptchaClassification(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            queries=[self.image_body],
            question=self.question,
        ).captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution
"""
