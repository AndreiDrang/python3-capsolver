import os
import time
import base64
import random
import string

import pytest


@pytest.fixture(scope="function")
def delay_func():
    time.sleep(1)


@pytest.fixture(scope="class")
def delay_class():
    time.sleep(2)


@pytest.mark.usefixtures("delay_func")
@pytest.mark.usefixtures("delay_class")
class BaseTest:
    image_captcha_path_example = "tests/files/captcha_example.jpeg"
    image_captcha_url_example = (
        "https://github.com/AndreiDrang/python3-capsolver/blob/main/tests/files/captcha_example.jpeg?raw=true"
    )

    API_KEY = os.environ["API_KEY"]
    sleep_time = 5

    proxyTypes = ["socks5", "http", "https"]
    proxyAddress = "0.0.0.0"
    proxyPort = 9999

    @staticmethod
    def get_random_string(length: int = 36) -> str:
        """
        Method generate random string with set length

        Args:
            length: Len of generated string

        Returns:
            Random letter string
        """
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for _ in range(length))
        return result_str

    def read_image(self) -> bytes:
        with open(self.image_captcha_path_example, "rb") as img_file:
            return img_file.read()

    def read_image_as_str(self) -> str:
        return base64.b64encode(self.read_image()).decode("utf-8")
