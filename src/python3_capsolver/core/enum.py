from enum import Enum
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


class EndpointPostfixEnm(str, MyEnum):
    """
    Enum stored URL postfixes for API endpoints
    """

    GET_BALANCE = "getBalance"
    CREATE_TASK = "createTask"
    GET_TASK_RESULT = "getTaskResult"
    AKAMAI_BMP_INVOKE = "akamaibmp/invoke"
    AKAMAI_WEB_INVOKE = "akamaiweb/invoke"


class CaptchaTypeEnm(str, MyEnum):
    Control = "Control"

    ImageToTextTask = "ImageToTextTask"
    VisionEngine = "VisionEngine"

    HCaptchaTask = "HCaptchaTask"
    HCaptchaTaskProxyless = "HCaptchaTaskProxyless"
    HCaptchaEnterpriseTask = "HCaptchaEnterpriseTask"
    HCaptchaEnterpriseTaskProxyLess = "HCaptchaEnterpriseTaskProxyLess"
    HCaptchaTurboTask = "HCaptchaTurboTask"
    HCaptchaClassification = "HCaptchaClassification"

    FunCaptchaTask = "FunCaptchaTask"
    FunCaptchaTaskProxyLess = "FunCaptchaTaskProxyLess"

    FunCaptchaClassification = "FunCaptchaClassification"

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

    AntiCloudflareTask = "AntiCloudflareTask"

    AntiAwsWafTask = "AntiAwsWafTask"
    AntiAwsWafTaskProxyLess = "AntiAwsWafTaskProxyLess"
    AwsWafClassification = "AwsWafClassification"

    AntiCyberSiAraTask = "AntiCyberSiAraTask"
    AntiCyberSiAraTaskProxyLess = "AntiCyberSiAraTaskProxyLess"

    AntiAkamaiBMPTask = "AntiAkamaiBMPTask"
    AntiAkamaiWebTask = "AntiAkamaiWebTask"

    AntiImpervaTask = "AntiImpervaTask"

    BinanceCaptchaTask = "BinanceCaptchaTask"


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


class SaveFormatsEnm(str, MyEnum):
    TEMP = "temp"
    CONST = "const"
