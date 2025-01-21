import urllib3
from tenacity import AsyncRetrying, wait_fixed, stop_after_attempt
from requests.adapters import Retry

__all__ = (
    "APP_ID",
    "RETRIES",
    "REQUEST_URL",
    "ASYNC_RETRIES",
    "VALID_STATUS_CODES",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RETRIES = Retry(total=5, backoff_factor=0.9, status_forcelist=[500, 502, 503, 504])
ASYNC_RETRIES = AsyncRetrying(wait=wait_fixed(5), stop=stop_after_attempt(5), reraise=True)

REQUEST_URL = "https://api.capsolver.com"
VALID_STATUS_CODES = (200, 202, 400, 401, 405)

APP_ID = "3E36E3CD-7EB5-4CAF-AA15-91011E652321"
