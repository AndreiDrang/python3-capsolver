from typing import Any, Dict, List, Optional

from pydantic import Field, BaseModel, conint, constr

from python3_captchaai.core.enum import ProxyType, CaptchaTypeEnm, ResponseStatusEnm

"""
HTTP API Request ser
"""


class PostRequestSer(BaseModel):
    clientKey: str = Field(..., description="Client account key, can be found in user account")


class TaskSer(BaseModel):
    type: CaptchaTypeEnm = Field(..., description="Task type name")


class RequestCreateTaskSer(PostRequestSer):
    task: Optional[TaskSer] = Field(None, description="Task object")


class RequestGetTaskResultSer(PostRequestSer):
    taskId: Optional[str] = Field(None, description="ID created by the createTask method")


"""
HTTP API Response ser
"""


class ResponseSer(BaseModel):
    errorId: bool = Field(False, description="Error message: `False` - no error, `True` - with error")
    # error info
    errorCode: Optional[str] = Field(None, description="Error code")
    errorDescription: Optional[str] = Field(None, description="Error description")


class CaptchaResponseSer(ResponseSer):
    taskId: Optional[str] = Field(None, description="Task ID for future use in getTaskResult method.")
    # TODO check docs, this field some times is `status` and some times its `state`
    status: ResponseStatusEnm = Field(ResponseStatusEnm.Processing, description="Task current status", alias="state")
    solution: Dict[str, Any] = Field(None, description="Task result data. Different for each type of task.")

    class Config:
        allow_population_by_field_name = True


class ControlResponseSer(ResponseSer):
    balance: Optional[float] = Field(0, description="Account balance value in USD")
    packages: List = Field(None, description="Monthly Packages")


"""
Other ser
"""


class CaptchaOptionsSer(BaseModel):
    api_key: constr(min_length=36, max_length=36)
    sleep_time: conint(ge=5)


"""
ReCaptcha ser
"""


class WebsiteDataOptionsSer(BaseModel):
    websiteURL: str = Field(..., description="Address of a webpage with Google ReCaptcha")
    websiteKey: str = Field(
        ..., description="Recaptcha website key. <div class='g-recaptcha' data-sitekey='THAT_ONE'></div>"
    )


class ProxyDataOptionsSer(WebsiteDataOptionsSer):
    proxyType: ProxyType = Field(..., description="Type of the proxy")
    proxyAddress: str = Field(
        ...,
        description="Proxy IP address IPv4/IPv6."
        "Not allowed to use:"
        "host names instead of IPs,"
        "transparent proxies (where client IP is visible),"
        "proxies from local networks (192.., 10.., 127...)",
    )
    proxyPort: int = Field(..., description="Proxy port.")


class ReCaptchaV3ProxyLessOptionsSer(WebsiteDataOptionsSer):
    pageAction: str = Field(
        "verify",
        description="Widget action value."
        "Website owner defines what user is doing on the page through this parameter",
    )


class ReCaptchaV3OptionsSer(ReCaptchaV3ProxyLessOptionsSer, ProxyDataOptionsSer):
    pass


class HCaptchaOptionsSer(BaseModel):
    queries: List[str] = Field(..., description="Base64-encoded images, do not include 'data:image/***;base64,'")
    question: str = Field(
        ..., description="Question ID. Support English and Chinese, other languages please convert yourself"
    )
