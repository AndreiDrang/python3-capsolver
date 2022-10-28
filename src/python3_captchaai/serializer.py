from uuid import uuid4
from typing import Union, Optional

from pydantic import Field, BaseModel, validator, root_validator, conint

from . import enums

"""
HTTP API Serializers
"""


class PostRequestSer(BaseModel):
    clientKey: str


class GetRequestSer(BaseModel):
    clientKey: str


class CaptchaOptionsSer(BaseModel):
    api_key: str
    sleep_time: conint(ge=5) = 5

    url_request: str = ""
    url_response: str = ""


"""
HTTP API Response
"""


class ServicePostResponseSer(BaseModel):
    status: int
    request: str


class ServiceGetResponseSer(BaseModel):
    status: int
    request: Union[str, dict]

    # ReCaptcha V3 params
    user_check: str = ""
    user_score: str = ""


class ResponseSer(BaseModel):
    balance: Optional[float] = 0
    # error info
    error: bool
    ErrorCode: str
    errorDescription: str
