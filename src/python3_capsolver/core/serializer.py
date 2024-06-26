from typing import Any, Dict, List, Literal, Optional

from pydantic import Field, BaseModel, conint

from python3_capsolver.core.enum import ResponseStatusEnm
from python3_capsolver.core.config import APP_ID

"""
HTTP API Request ser
"""


class PostRequestSer(BaseModel):
    clientKey: str = Field(..., description="Client account key, can be found in user account")
    task: dict = Field(None, description="Task object")


class TaskSer(BaseModel):
    type: str = Field(..., description="Task type name", alias="captcha_type")


class RequestCreateTaskSer(PostRequestSer):
    appId: Literal[APP_ID] = APP_ID


class RequestGetTaskResultSer(PostRequestSer):
    taskId: Optional[str] = Field(None, description="ID created by the createTask method")


"""
HTTP API Response ser
"""


class ResponseSer(BaseModel):
    errorId: int = Field(..., description="Error message: `False` - no error, `True` - with error")
    # error info
    errorCode: Optional[str] = Field(None, description="Error code")
    errorDescription: Optional[str] = Field(None, description="Error description")


class CaptchaResponseSer(ResponseSer):
    taskId: Optional[str] = Field(None, description="Task ID for future use in getTaskResult method.")
    status: ResponseStatusEnm = Field(ResponseStatusEnm.Processing, description="Task current status")
    solution: Dict[str, Any] = Field(None, description="Task result data. Different for each type of task.")

    class Config:
        populate_by_name = True


class ControlResponseSer(ResponseSer):
    balance: Optional[float] = Field(0, description="Account balance value in USD")


"""
Other ser
"""


class CaptchaOptionsSer(BaseModel):
    api_key: str
    sleep_time: conint(ge=5) = 5


"""
Captcha tasks ser
"""


class WebsiteDataOptionsSer(TaskSer):
    websiteURL: str = Field(..., description="Address of a webpage with Captcha")
    websiteKey: Optional[str] = Field(None, description="Website key")


class ReCaptchaV3Ser(WebsiteDataOptionsSer):
    pageAction: str = Field(
        "verify",
        description="Widget action value."
        "Website owner defines what user is doing on the page through this parameter",
    )


class HCaptchaClassificationOptionsSer(TaskSer):
    queries: List[str] = Field(..., description="Base64-encoded images, do not include 'data:image/***;base64,'")
    question: str = Field(
        ..., description="Question ID. Support English and Chinese, other languages please convert yourself"
    )


class FunCaptchaClassificationOptionsSer(TaskSer):
    images: List[str] = Field(..., description="Base64-encoded images, do not include 'data:image/***;base64,'")
    question: str = Field(
        ...,
        description="Question name. this param value from API response game_variant field. Exmaple: maze,maze2,flockCompass,3d_rollball_animals",
    )


class GeeTestSer(TaskSer):
    websiteURL: str = Field(..., description="Address of a webpage with Geetest")
    gt: str = Field(..., description="The domain public key, rarely updated")
    challenge: Optional[str] = Field(
        "",
        description="If you need to solve Geetest V3 you must use this parameter, don't need if you need to solve GeetestV4",
    )


class FunCaptchaSer(TaskSer):
    websiteURL: str = Field(..., description="Address of a webpage with Funcaptcha")
    websitePublicKey: str = Field(..., description="Funcaptcha website key.")
    funcaptchaApiJSSubdomain: Optional[str] = Field(
        None,
        description="A special subdomain of funcaptcha.com, from which the JS captcha widget should be loaded."
        "Most FunCaptcha installations work from shared domains.",
    )


class DatadomeSliderSer(TaskSer):
    websiteURL: str = Field(..., description="Address of a webpage with DatadomeSlider")
    captchaUrl: str = Field(..., description="Captcha Url where is the captcha")
    userAgent: str = Field(..., description="Browser's User-Agent which is used in emulation")


class CloudflareTurnstileSer(WebsiteDataOptionsSer): ...


class CyberSiAraSer(WebsiteDataOptionsSer):
    SlideMasterUrlId: str = Field(
        ..., description="You can get MasterUrlId param form `api/CyberSiara/GetCyberSiara` endpoint request"
    )
    UserAgent: str = Field(..., description="Browser userAgent, you need submit your userAgent")


class AntiAkamaiBMPTaskSer(TaskSer):
    packageName: str = Field("de.zalando.iphone", description="Package name of AkamaiBMP mobile APP")
    version: str = Field("3.2.6", description="AKAMAI BMP Version number")
    country: str = Field("US", description="AKAMAI BMP country")


class AntiAkamaiWebTaskSer(TaskSer):
    url: str = Field(..., description="Browser url address")


class AntiImpervaTaskSer(TaskSer):
    websiteUrl: str = Field(..., description="The website url")
    userAgent: str = Field(..., description="Browser userAgent")
    utmvc: bool = Field(
        True, description="If cookie contains `incap_see_xxx`, `nlbi_xxx`, `visid_inap_xxx`, mean is true"
    )
    reese84: bool = Field(True, description="if cookie conains `reese84`, set it true")


class BinanceCaptchaTaskSer(TaskSer):
    websiteURL: str = Field(..., description="Address of a webpage with Binance captcha")
    websiteKey: str = Field("login", description="`bizId` always be `login`")
    validateId: str = Field(..., description="`validateId` bncaptcha validateId field")
