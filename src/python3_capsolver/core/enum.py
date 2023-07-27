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
    """

    GET_BALANCE = "getBalance"
    CREATE_TASK = "createTask"
    GET_TASK_RESULT = "getTaskResult"


class ImageToTextTaskTypeEnm(str, MyEnum):
    ImageToTextTask = "ImageToTextTask"


class HCaptchaTypeEnm(str, MyEnum):
    HCaptchaTask = "HCaptchaTask"
    HCaptchaTaskProxyless = "HCaptchaTaskProxyless"
    HCaptchaEnterpriseTask = "HCaptchaEnterpriseTask"
    HCaptchaEnterpriseTaskProxyLess = "HCaptchaEnterpriseTaskProxyLess"
    HCaptchaTurboTask = "HCaptchaTurboTask"
    HCaptchaClassification = "HCaptchaClassification"


class HCaptchaClassificationTypeEnm(str, MyEnum):
    HCaptchaClassification = "HCaptchaClassification"


class FunCaptchaTypeEnm(str, MyEnum):
    FunCaptchaTask = "FunCaptchaTask"
    FunCaptchaTaskProxyLess = "FunCaptchaTaskProxyLess"


class FunCaptchaClassificationTypeEnm(str, MyEnum):
    FunCaptchaClassification = "FunCaptchaClassification"


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


class AntiAwsWafTaskTypeEnm(str, MyEnum):
    AntiAwsWafTask = "AntiAwsWafTask"
    AntiAwsWafTaskProxyLess = "AntiAwsWafTaskProxyLess"


class AntiCyberSiAraTaskTypeEnm(str, MyEnum):
    AntiCyberSiAraTask = "AntiCyberSiAraTask"
    AntiCyberSiAraTaskProxyLess = "AntiCyberSiAraTaskProxyLess"


class ResponseStatusEnm(str, MyEnum):
    """
    Enum store results `status` field variants

    Notes:
        https://docs.capsolver.com/guide/api-createtask.html
    """

    Idle = "idle"  # Task created
    Processing = "processing"  # Task is not ready yet
    Ready = "ready"  # Task completed, solution object can be found in solution property
    Failed = "failed"  # Task failed, check the errorDescription to know why failed.
