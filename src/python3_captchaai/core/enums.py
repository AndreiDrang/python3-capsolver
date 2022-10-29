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


class CaptchaControlEnm(MyEnum):
    # https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426080/getBalance+retrieve+account+balance
    GET_BALANCE = "getBalance"


class CaptchaTypeEnm(MyEnum):
    ImageToTextTask = "ImageToTextTask"
    # Recaptcha
    ReCaptchaV2TaskProxyLess = "ReCaptchaV2TaskProxyLess"
    ReCaptchaV2Task = "ReCaptchaV2Task"
    ReCaptchaV2EnterpriseTask = "ReCaptchaV2EnterpriseTask"
    ReCaptchaV2EnterpriseTaskProxyless = "ReCaptchaV2EnterpriseTaskProxyless"
    ReCaptchaV3Task = "ReCaptchaV3Task"
    ReCaptchaV3TaskProxyless = "ReCaptchaV3TaskProxyless"
    # HCaptcha
    HCaptchaTask = "HCaptchaTask"
    HCaptchaTaskProxyless = "HCaptchaTaskProxyless"
    HCaptchaClassification = "HCaptchaClassification"
    # GeeTest
    GeetestTask = "GeetestTask"
    GeetestTaskProxyless = "GeetestTaskProxyless"
    # FunCaptcha
    FunCaptchaClassification = "FunCaptchaClassification"
    FuncaptchaTask = "FuncaptchaTask"
    FuncaptchaTaskProxyless = "FuncaptchaTaskProxyless"
    # Other types
    DatadomeSliderTask = "DatadomeSliderTask"
    AntiKasadaTask = "AntiKasadaTask"
    AntiAkamaiBMPTask = "AntiAkamaiBMPTask"
