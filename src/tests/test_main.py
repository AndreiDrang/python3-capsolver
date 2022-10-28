from tenacity import AsyncRetrying
from urllib3.util.retry import Retry

from src.tests.conftest import CoreTest
from src.python3_captchaai.config import RETRIES, ASYNC_RETRIES


class TestMain(CoreTest):
    """
    Success tests
    """

    def test_reties(self):
        assert isinstance(RETRIES, Retry)

    def test_async_reties(self):
        assert isinstance(ASYNC_RETRIES, AsyncRetrying)
