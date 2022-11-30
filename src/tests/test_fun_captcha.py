import base64

import pytest
from pydantic import ValidationError

from src.tests.conftest import BaseTest
from python3_captchaai.core.enum import CaptchaTypeEnm, ResponseStatusEnm
from python3_captchaai.fun_captcha import FunCaptcha
from python3_captchaai.core.serializer import CaptchaResponseSer

websiteURL = "https://api.funcaptcha.com/fc/api/nojs/"
websitePublicKey = "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC"
funcaptchaApiJSSubdomain = "https://api.funcaptcha.com/"

with open("tests/files/fun_class.png", "rb") as img_file:
    img_data = img_file.read()

captcha_types = (
    CaptchaTypeEnm.FuncaptchaTask,
    CaptchaTypeEnm.FuncaptchaTaskProxyless,
    CaptchaTypeEnm.FunCaptchaClassification,
)


class TestFunCaptchaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in FunCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in FunCaptcha.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            FunCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=CaptchaTypeEnm.Control,
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            ).captcha_handler()

    @pytest.mark.parametrize("captcha_type", captcha_types)
    def test_wrong_type_params(self, captcha_type: str):
        with pytest.raises(expected_exception=(ValidationError, ValueError)):
            FunCaptcha(api_key=self.get_random_string(36), captcha_type=captcha_type).captcha_handler()

    @pytest.mark.parametrize("captcha_type", captcha_types)
    async def test_aio_wrong_type_params(self, captcha_type: str):
        with pytest.raises(expected_exception=(ValidationError, ValueError)):
            await FunCaptcha(api_key=self.get_random_string(36), captcha_type=captcha_type).aio_captcha_handler()

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            FunCaptcha(
                api_key=self.get_random_string(36),
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            )


class TestFunCaptchaProxyless(BaseTest):

    captcha_type = CaptchaTypeEnm.FuncaptchaTaskProxyless
    """
    Success tests
    """

    def test_params(self):
        FunCaptcha(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=websiteURL,
            websitePublicKey=websitePublicKey,
            funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
        )

    def test_params_context(self):
        with FunCaptcha(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=websiteURL,
            websitePublicKey=websitePublicKey,
            funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
        ) as instance:
            pass

    def test_solve(self):
        resp = FunCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=websiteURL,
            websitePublicKey=websitePublicKey,
            funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
        ).captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Processing)
        assert resp.errorId in (False, True)
        assert resp.errorCode in (None, "ERROR_ZERO_BALANCE")
        assert resp.errorDescription in (None, "Your service balance is insufficient.")

    def test_solve_context(self):
        with FunCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=websiteURL,
            websitePublicKey=websitePublicKey,
            funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
        ) as instance:
            resp = instance.captcha_handler()
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Processing)
            assert resp.errorId in (False, True)
            assert resp.errorCode in (None, "ERROR_ZERO_BALANCE")
            assert resp.errorDescription in (None, "Your service balance is insufficient.")

    async def test_aio_solve(self):
        resp = await FunCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=websiteURL,
            websitePublicKey=websitePublicKey,
            funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
        ).aio_captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Processing)
        assert resp.errorId in (False, True)
        assert resp.errorCode in (None, "ERROR_ZERO_BALANCE")
        assert resp.errorDescription in (None, "Your service balance is insufficient.")

    async def test_aio_solve_context(self):
        with FunCaptcha(
            api_key=self.API_KEY,
            captcha_type=self.captcha_type,
            websiteURL=websiteURL,
            websitePublicKey=websitePublicKey,
            funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
        ) as instance:
            resp = await instance.aio_captcha_handler()
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status in (ResponseStatusEnm.Ready, ResponseStatusEnm.Processing)
            assert resp.errorId in (False, True)
            assert resp.errorCode in (None, "ERROR_ZERO_BALANCE")
            assert resp.errorDescription in (None, "Your service balance is insufficient.")

    """
    Failed tests
    """

    def test_no_website_key(self):
        with pytest.raises(ValidationError):
            FunCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=websiteURL,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            )

    def test_no_website_url(self):
        with pytest.raises(ValidationError):
            FunCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            )

    def test_no_api_js(self):
        with pytest.raises(ValidationError):
            FunCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
            )

    async def test_aio_api_key_err(self):
        with pytest.raises(Exception):
            await FunCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            ).aio_captcha_handler()

    def test_api_key_err(self):
        with pytest.raises(Exception):
            FunCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.captcha_type,
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            ).captcha_handler()


class TestFunCaptchaClassification(BaseTest):

    captcha_type = CaptchaTypeEnm.FunCaptchaClassification

    question = "Pick the bicycle"
    image = base64.b64encode(img_data).decode("utf-8")
    """
    Success tests
    """

    def test_params(self):
        FunCaptcha(api_key=self.get_random_string(36), captcha_type=self.captcha_type)

    def test_params_context(self):
        with FunCaptcha(api_key=self.get_random_string(36), captcha_type=self.captcha_type) as instance:
            pass

    def test_solve(self):
        resp = FunCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type).captcha_handler(
            image=self.image, question=self.question
        )
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId is True
        """assert resp.errorId is False
        assert resp.errorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None"""

    def test_solve_context(self):
        with FunCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type) as instance:
            resp = instance.captcha_handler(image=self.image, question=self.question)
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status == ResponseStatusEnm.Processing
            assert resp.errorId is True
            """assert resp.errorId is False
            assert resp.errorCode is None
            assert resp.errorDescription is None
            assert resp.solution is not None"""

    async def test_aio_solve(self):
        resp = await FunCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type).aio_captcha_handler(
            image=self.image, question=self.question
        )
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId is True
        """assert resp.errorId is False
        assert resp.errorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None"""

    async def test_aio_solve_context(self):
        with FunCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type) as instance:
            resp = await instance.aio_captcha_handler(image=self.image, question=self.question)
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status == ResponseStatusEnm.Processing
            assert resp.errorId is True
            """assert resp.errorId is False
            assert resp.errorCode is None
            assert resp.errorDescription is None
            assert resp.solution is not None"""

    """
    Failed tests
    """

    def test_no_image(self):
        with pytest.raises(ValueError):
            FunCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type).captcha_handler(question=self.question)

    def test_no_question(self):
        with pytest.raises(ValueError):
            FunCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type).captcha_handler(image=self.image)

    async def test_aio_no_image(self):
        with pytest.raises(ValueError):
            await FunCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type).aio_captcha_handler(
                question=self.question
            )

    async def test_aio_no_question(self):
        with pytest.raises(ValueError):
            await FunCaptcha(api_key=self.API_KEY, captcha_type=self.captcha_type).aio_captcha_handler(image=self.image)
