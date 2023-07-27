import base64

import pytest
from pydantic import ValidationError

from tests.conftest import BaseTest
from python3_capsolver.core.enum import FunCaptchaTypeEnm, ResponseStatusEnm, FunCaptchaClassificationTypeEnm
from python3_capsolver.fun_captcha import FunCaptcha, FunCaptchaClassification
from python3_capsolver.core.serializer import CaptchaResponseSer

websiteURL = "https://api.funcaptcha.com/fc/api/nojs/"
websitePublicKey = "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC"
funcaptchaApiJSSubdomain = "https://api.funcaptcha.com/"

with open("tests/files/fun_class.png", "rb") as img_file:
    img_data = img_file.read()


class TestFunCaptchaBase(BaseTest):
    def test_captcha_handler_exist(self):
        assert "captcha_handler" in FunCaptcha.__dict__.keys()

    def test_aio_captcha_handler_exist(self):
        assert "aio_captcha_handler" in FunCaptcha.__dict__.keys()

    def test_wrong_captcha_type(self):
        with pytest.raises(ValueError):
            FunCaptcha(
                api_key=self.get_random_string(36),
                captcha_type="test",
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            ).captcha_handler()

    def test_wrong_type_params(self):
        with pytest.raises(expected_exception=(ValidationError, ValueError)):
            FunCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.get_random_string(5),
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
            ).captcha_handler()

    async def test_aio_wrong_type_params(self):
        with pytest.raises(expected_exception=(ValidationError, ValueError)):
            await FunCaptcha(
                api_key=self.get_random_string(36),
                captcha_type=self.get_random_string(5),
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
            ).aio_captcha_handler()

    def test_no_captcha_type(self):
        with pytest.raises(TypeError):
            FunCaptcha(
                api_key=self.get_random_string(36),
                websiteURL=websiteURL,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            )


class TestFunCaptchaProxyless(BaseTest):
    captcha_type = FunCaptchaTypeEnm.FunCaptchaTaskProxyLess
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

    """    def test_solve(self):
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
    """
    Failed tests
    """

    def test_no_website_key(self):
        with pytest.raises(TypeError):
            FunCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websiteURL=websiteURL,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            )

    def test_no_website_url(self):
        with pytest.raises(TypeError):
            FunCaptcha(
                api_key=self.API_KEY,
                captcha_type=self.captcha_type,
                websitePublicKey=websitePublicKey,
                funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
            )

    async def test_aio_api_key_err(self):
        result = await FunCaptcha(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=websiteURL,
            websitePublicKey=websitePublicKey,
            funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
        ).aio_captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution

    def test_api_key_err(self):
        result = FunCaptcha(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            websiteURL=websiteURL,
            websitePublicKey=websitePublicKey,
            funcaptchaApiJSSubdomain=funcaptchaApiJSSubdomain,
        ).captcha_handler()
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
        assert not result.solution


class TestFunCaptchaClassification(BaseTest):
    captcha_type = FunCaptchaClassificationTypeEnm.FunCaptchaClassification

    question = "maze"
    images = [base64.b64encode(img_data).decode("utf-8")]
    """
    Success tests
    """

    def test_params(self):
        FunCaptchaClassification(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            images=self.images,
            question=self.question,
        )

    def test_params_context(self):
        with FunCaptchaClassification(
            api_key=self.get_random_string(36),
            captcha_type=self.captcha_type,
            images=self.images,
            question=self.question,
        ) as instance:
            pass

    def test_solve(self):
        resp = FunCaptchaClassification(
            api_key=self.API_KEY, captcha_type=self.captcha_type, images=self.images, question=self.question
        ).captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId == 1
        """assert resp.errorId == 0
        assert resp.errorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None"""

    def test_solve_context(self):
        with FunCaptchaClassification(
            api_key=self.API_KEY, captcha_type=self.captcha_type, images=self.images, question=self.question
        ) as instance:
            resp = instance.captcha_handler()
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status == ResponseStatusEnm.Processing
            assert resp.errorId == 1
            """assert resp.errorId == 0
            assert resp.errorCode is None
            assert resp.errorDescription is None
            assert resp.solution is not None"""

    async def test_aio_solve(self):
        resp = await FunCaptchaClassification(
            api_key=self.API_KEY, captcha_type=self.captcha_type, images=self.images, question=self.question
        ).aio_captcha_handler()
        assert isinstance(resp, CaptchaResponseSer)
        assert resp.status == ResponseStatusEnm.Processing
        assert resp.errorId == 1
        """assert resp.errorId == 0
        assert resp.errorCode is None
        assert resp.errorDescription is None
        assert resp.solution is not None"""

    async def test_aio_solve_context(self):
        with FunCaptchaClassification(
            api_key=self.API_KEY, captcha_type=self.captcha_type, images=self.images, question=self.question
        ) as instance:
            resp = await instance.aio_captcha_handler()
            assert isinstance(resp, CaptchaResponseSer)
            assert resp.status == ResponseStatusEnm.Processing
            assert resp.errorId == 1
            """assert resp.errorId == 0
            assert resp.errorCode is None
            assert resp.errorDescription is None
            assert resp.solution is not None"""

    """
    Failed tests
    """

    def test_no_image(self):
        with pytest.raises(TypeError):
            FunCaptchaClassification(
                api_key=self.API_KEY, captcha_type=self.captcha_type, question=self.question
            ).captcha_handler()

    def test_no_question(self):
        with pytest.raises(TypeError):
            FunCaptchaClassification(
                api_key=self.API_KEY, captcha_type=self.captcha_type, images=self.images
            ).captcha_handler()

    def test_wrong_type_params(self):
        with pytest.raises(expected_exception=(ValidationError, ValueError)):
            FunCaptchaClassification(
                api_key=self.API_KEY,
                captcha_type=self.get_random_string(36),
                images=self.images,
                question=self.question,
            ).captcha_handler()

    async def test_aio_wrong_type_params(self):
        with pytest.raises(expected_exception=(ValidationError, ValueError)):
            FunCaptchaClassification(
                api_key=self.API_KEY,
                captcha_type=self.get_random_string(36),
                images=self.images,
                question=self.question,
            ).captcha_handler()
