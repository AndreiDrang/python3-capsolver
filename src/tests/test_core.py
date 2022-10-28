import pytest
from tenacity import AsyncRetrying
from urllib3.util.retry import Retry

from tests.conftest import BaseTest
from python3_captchaai.control import Control
from python3_captchaai.core.config import RETRIES, ASYNC_RETRIES


class TestCore(BaseTest):
    """
    Success tests
    """

    def test_reties(self):
        assert isinstance(RETRIES, Retry)

    def test_async_reties(self):
        assert isinstance(ASYNC_RETRIES, AsyncRetrying)

    @pytest.mark.parametrize("api_len", [35, 37])
    async def test_wrong_key_err(self, api_len: int):
        with pytest.raises(ValueError):
            await Control(api_key=self.get_random_string(api_len)).aio_get_balance()
