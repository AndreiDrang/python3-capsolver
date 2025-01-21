from enum import Enum
from typing import List

__all__ = ("EndpointPostfixEnm", "CaptchaTypeEnm", "ResponseStatusEnm", "SaveFormatsEnm")


class MyEnum(str, Enum):
    @classmethod
    def list(cls) -> List[Enum]:
        return list(map(lambda c: c, cls))

    @classmethod
    def list_values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls) -> List[str]:
        return list(map(lambda c: c.name, cls))


class EndpointPostfixEnm(MyEnum):
    """
    Enum stored URL postfixes for API endpoints
    """

    GET_BALANCE = "getBalance"
    CREATE_TASK = "createTask"
    GET_TASK_RESULT = "getTaskResult"
    GET_TOKEN = "getToken"
    FEEDBACK_TASK = "feedbackTask"


class CaptchaTypeEnm(MyEnum):
    Control = "Control"

    ImageToTextTask = "ImageToTextTask"
    VisionEngine = "VisionEngine"

    GeeTestTaskProxyLess = "GeeTestTaskProxyLess"

    # re-captcha
    ReCaptchaV2Classification = "ReCaptchaV2Classification"
    ReCaptchaV2Task = "ReCaptchaV2Task"
    ReCaptchaV2EnterpriseTask = "ReCaptchaV2EnterpriseTask"
    ReCaptchaV2TaskProxyLess = "ReCaptchaV2TaskProxyLess"
    ReCaptchaV2EnterpriseTaskProxyLess = "ReCaptchaV2EnterpriseTaskProxyLess"

    ReCaptchaV3Task = "ReCaptchaV3Task"
    ReCaptchaV3EnterpriseTask = "ReCaptchaV3EnterpriseTask"
    ReCaptchaV3TaskProxyLess = "ReCaptchaV3TaskProxyLess"
    ReCaptchaV3EnterpriseTaskProxyLess = "ReCaptchaV3EnterpriseTaskProxyLess"

    MtCaptchaTask = "MtCaptchaTask"
    MtCaptchaTaskProxyLess = "MtCaptchaTaskProxyLess"

    DatadomeSliderTask = "DatadomeSliderTask"

    AntiTurnstileTaskProxyLess = "AntiTurnstileTaskProxyLess"
    AntiCloudflareTask = "AntiCloudflareTask"

    FriendlyCaptchaTaskProxyless = "FriendlyCaptchaTaskProxyless"

    YandexCaptchaTaskProxyLess = "YandexCaptchaTaskProxyLess"

    AntiAwsWafTask = "AntiAwsWafTask"
    AntiAwsWafTaskProxyLess = "AntiAwsWafTaskProxyLess"
    AwsWafClassification = "AwsWafClassification"


class ResponseStatusEnm(MyEnum):
    """
    Enum store results `status` field variants

    Notes:
        https://docs.capsolver.com/guide/api-createtask.html
    """

    Idle = "idle"  # Task created
    Processing = "processing"  # Task is not ready yet
    Ready = "ready"  # Task completed, solution object can be found in solution property
    Failed = "failed"  # Task failed, check the errorDescription to know why failed.


class SaveFormatsEnm(MyEnum):
    TEMP = "temp"
    CONST = "const"
