from tests.conftest import BaseTest
from python3_capsolver.control import Control
from python3_capsolver.core.serializer import ControlResponseSer


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
        assert resp.errorId == 0
        assert resp.errorCode is None
        assert resp.errorDescription is None

    async def test_aio_get_balance(self):
        resp = await Control(api_key=self.API_KEY).aio_get_balance()
        assert isinstance(resp, ControlResponseSer)
        assert resp.errorId == 0
        assert resp.errorCode is None
        assert resp.errorDescription is None

    """
    Failed tests
    """

    def test_get_balance_api_key_err(self):
        result = Control(api_key=self.get_random_string(36)).get_balance()
        assert isinstance(result, ControlResponseSer)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"

    async def test_aio_get_balance_api_key_err(self):
        result = await Control(api_key=self.get_random_string(36)).aio_get_balance()
        assert isinstance(result, ControlResponseSer)
        assert result.errorId == 1
        assert result.errorCode == "ERROR_KEY_DENIED_ACCESS"
