from tenacity import AsyncRetrying, wait_fixed, stop_after_attempt
from requests.adapters import Retry

RETRIES = Retry(total=5, backoff_factor=0.9, status_forcelist=[500, 502, 503, 504])
ASYNC_RETRIES = AsyncRetrying(wait=wait_fixed(5), stop=stop_after_attempt(5), reraise=True)

REQUEST_URL = "https://api.captchaai.io"
VALID_STATUS_CODES = (200, 400)
