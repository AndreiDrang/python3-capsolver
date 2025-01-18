import pytest

from tests.conftest import BaseTest
from python3_capsolver.control import Control


class TestControl(BaseTest):
    """
    Success tests
    """

    def test_get_balance_exist(self):
        assert "get_balance" in Control.__dict__.keys()
        assert "aio_get_balance" in Control.__dict__.keys()

    def test_get_balance(self):
        result = Control(api_key=self.API_KEY).get_balance()
        assert isinstance(result, dict)
        assert result["errorId"] == 0
        assert result["balance"] != 0.0

    async def test_aio_get_balance(self):
        result = await Control(api_key=self.API_KEY).aio_get_balance()
        assert isinstance(result, dict)
        assert result["errorId"] == 0
        assert result["balance"] != 0.0

    """
    Failed tests
    """

    def test_get_balance_api_key_err(self):
        with pytest.raises(ValueError):
            Control(api_key=self.get_random_string(36)).get_balance()

    async def test_aio_get_balance_api_key_err(self):
        with pytest.raises(ValueError):
            await Control(api_key=self.get_random_string(36)).aio_get_balance()
