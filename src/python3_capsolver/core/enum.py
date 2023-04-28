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
        """
        The name of the Enum member
        """
        return self._name_

    @DynamicClassAttribute
    def value(self) -> str:
        """
        The name of the Enum member
        """
        return self._value_


class EndpointPostfixEnm(str, MyEnum):
    """
    Enum stored URL postfixes for API endpoints

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426042
    """

    GET_BALANCE = "getBalance"
    CREATE_TASK = "createTask"
    GET_TASK_RESULT = "getTaskResult"


class CaptchaTypeEnmXXX(str, MyEnum):
    """
    Enum with all available captcha types

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/393295
    """

    ImageToTextTask = "ImageToTextTask"
    # HCaptcha
    HCaptchaClassification = "HCaptchaClassification"
    # FunCaptcha
    FunCaptchaClassification = "FunCaptchaClassification"
    # Other types
    AntiKasadaTask = "AntiKasadaTask"
    AntiAkamaiBMPTask = "AntiAkamaiBMPTask"


class HCaptchaTypeEnm(str, MyEnum):
    HCaptchaTask = "HCaptchaTask"
    HCaptchaTaskProxyless = "HCaptchaTaskProxyless"
    HCaptchaEnterpriseTask = "HCaptchaEnterpriseTask"
    HCaptchaEnterpriseTaskProxyLess = "HCaptchaEnterpriseTaskProxyLess"
    HCaptchaTurboTask = "HCaptchaTurboTask"
    HCaptchaTurboTaskProxyLess = "HCaptchaTurboTaskProxyLess"


class FunCaptchaTypeEnm(str, MyEnum):
    FunCaptchaTask = "FunCaptchaTask"
    FunCaptchaTaskProxyLess = "FunCaptchaTaskProxyLess"


class GeeTestCaptchaTypeEnm(str, MyEnum):
    GeeTestTask = "GeeTestTask"
    GeeTestTaskProxyLess = "GeeTestTaskProxyLess"


class ReCaptchaV2TypeEnm(str, MyEnum):
    # V2
    ReCaptchaV2Task = "ReCaptchaV2Task"
    ReCaptchaV2EnterpriseTask = "ReCaptchaV2EnterpriseTask"
    ReCaptchaV2TaskProxyLess = "ReCaptchaV2TaskProxyLess"
    ReCaptchaV2EnterpriseTaskProxyLess = "ReCaptchaV2EnterpriseTaskProxyLess"


class ReCaptchaV3TypeEnm(str, MyEnum):
    ReCaptchaV3Task = "ReCaptchaV3Task"
    ReCaptchaV3EnterpriseTask = "ReCaptchaV3EnterpriseTask"
    ReCaptchaV3TaskProxyLess = "ReCaptchaV3TaskProxyLess"
    ReCaptchaV3EnterpriseTaskProxyLess = "ReCaptchaV3EnterpriseTaskProxyLess"


class MtCaptchaTypeEnm(str, MyEnum):
    MtCaptchaTask = "MtCaptchaTask"
    MtCaptchaTaskProxyLess = "MtCaptchaTaskProxyLess"


class DatadomeSliderTypeEnm(str, MyEnum):
    DatadomeSliderTask = "DatadomeSliderTask"


class CloudflareTypeEnm(str, MyEnum):
    AntiCloudflareTask = "AntiCloudflareTask"


class ResponseStatusEnm(str, MyEnum):
    """
    Enum store results `status` field variants

    Notes:
        https://captchaai.atlassian.net/wiki/spaces/CAPTCHAAI/pages/426124
    """

    Idle = "idle"  # Task created
    Processing = "processing"  # Task is not ready yet
    Ready = "ready"  # Task completed, solution object can be found in solution property
    Failed = "failed"  # Task failed, check the errorDescription to know why failed.
