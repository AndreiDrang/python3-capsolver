from typing import Any, Dict, List, Literal, Optional

from msgspec import Struct

from .enum import ResponseStatusEnm
from .const import APP_ID


class MyBaseModel(Struct):
    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


"""
HTTP API Request ser
"""


class PostRequestSer(MyBaseModel):
    clientKey: str
    task: Dict = {}
    callbackUrl: Optional[str] = None


class TaskSer(MyBaseModel):
    type: str


class RequestCreateTaskSer(PostRequestSer):
    appId: Literal[APP_ID] = APP_ID


class RequestGetTaskResultSer(MyBaseModel):
    clientKey: str
    taskId: Optional[str] = None


"""
HTTP API Response ser
"""


class ResponseSer(MyBaseModel):
    errorId: int = 0
    # error info
    errorCode: Optional[str] = None
    errorDescription: Optional[str] = None


class CaptchaResponseSer(ResponseSer):
    taskId: Optional[str] = None
    status: ResponseStatusEnm = ResponseStatusEnm.Processing
    solution: Optional[Dict[str, Any]] = None


class ControlResponseSer(ResponseSer):
    balance: float = 0


"""
Other ser
"""


class CaptchaOptionsSer(MyBaseModel):
    api_key: str = None
    sleep_time: int = 5


"""
Captcha tasks ser
"""


class WebsiteDataOptionsSer(TaskSer):
    websiteURL: str
    websiteKey: Optional[str]


class ReCaptchaV3Ser(WebsiteDataOptionsSer):
    pageAction: str = "verify"


class HCaptchaClassificationOptionsSer(TaskSer):
    queries: List[str]
    question: str


class FunCaptchaClassificationOptionsSer(TaskSer):
    images: List[str]
    question: str


class GeeTestSer(TaskSer):
    websiteURL: str
    gt: str
    challenge: Optional[str] = ""


class FunCaptchaSer(TaskSer):
    websiteURL: str
    websitePublicKey: str
    funcaptchaApiJSSubdomain: Optional[str] = None


class DatadomeSliderSer(TaskSer):
    websiteURL: str
    captchaUrl: str
    userAgent: str


class CloudflareTurnstileSer(WebsiteDataOptionsSer): ...


class CyberSiAraSer(WebsiteDataOptionsSer):
    SlideMasterUrlId: str


class AntiAkamaiBMPTaskSer(TaskSer):
    packageName: str = "de.zalando.iphone"
    version: str = "3.2.6"
    country: str = "US"


class AntiAkamaiWebTaskSer(TaskSer):
    url: str


class AntiImpervaTaskSer(TaskSer):
    websiteUrl: str
    userAgent: str
    utmvc: bool = True
    reese84: bool = True


class BinanceCaptchaTaskSer(TaskSer):
    websiteURL: str
    validateId: str
    websiteKey: str = "login"
