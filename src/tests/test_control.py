import pytest

from tests.conftest import BaseTest
from python3_captchaai.control import Control
from python3_captchaai.core.serializer import ControlResponseSer


class TestControl(BaseTest):
    """
    Success tests
    """

    def test_get_balance_exist(self):
        assert "get_balance" in Control.__dict__.keys()

    def test_aio_get_balance_exist(self):
        assert "aio_get_balance" in Control.__dict__.keys()

    def test_get_balance(self):
        resp = Control(api_key=self.API_KEY).get_balance()
        assert isinstance(resp, ControlResponseSer)

    async def test_aio_get_balance(self):
        resp = await Control(api_key=self.API_KEY).aio_get_balance()
        assert isinstance(resp, ControlResponseSer)

    """
    Failed tests
    """

    def test_get_balance_api_key_err(self):
        with pytest.raises(Exception):
            Control(api_key=self.get_random_string(36)).get_balance()

    async def test_aio_get_balance_api_key_err(self):
        with pytest.raises(Exception):
            await Control(api_key=self.get_random_string(36)).aio_get_balance()
