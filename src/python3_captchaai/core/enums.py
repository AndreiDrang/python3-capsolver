from enum import Enum
from types import DynamicClassAttribute
from typing import List


class MyEnum(Enum):
    @classmethod
    def list(cls) -> List[Enum]:
        return list(map(lambda c: c, cls))

    @classmethod
    def list_values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls) -> List[str]:
        return list(map(lambda c: c.name, cls))

    @DynamicClassAttribute
    def name(self) -> str:
        """The name of the Enum member."""
        return self._name_

    @DynamicClassAttribute
    def value(self) -> str:
        """The name of the Enum member."""
        return self._value_


class SaveFormatsEnm(MyEnum):
    TEMP = "temp"
    CONST = "const"


class GeetestEnm(MyEnum):
    GEETEST = "geetest"
    GEETEST_V4 = "geetest_v4"


class ImageCaptchaEnm(MyEnum):
    BASE64 = "base64"


class CapyPuzzleEnm(MyEnum):
    CAPY = "capy"


class FunCaptchaEnm(MyEnum):
    FUNCAPTCHA = "funcaptcha"


class ReCaptchaEnm(MyEnum):
    USER_RECAPTCHA = "userrecaptcha"


class LeminCroppedCaptchaEnm(MyEnum):
    LEMIN = "lemin"


class HCaptchaEnm(MyEnum):
    HCAPTCHA = "hcaptcha"


class KeyCaptchaEnm(MyEnum):
    KEYCAPTCHA = "keycaptcha"


class RotateCaptchaEnm(MyEnum):
    ROTATECAPTCHA = "rotatecaptcha"


class TikTokCaptchaEnm(MyEnum):
    TIKTOK = "tiktok"


class CaptchaControlEnm(MyEnum):
    # https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426080/getBalance+retrieve+account+balance
    GET_BALANCE = "getBalance"


class YandexSmartCaptchaEnm(MyEnum):
    YANDEX = "yandex"
