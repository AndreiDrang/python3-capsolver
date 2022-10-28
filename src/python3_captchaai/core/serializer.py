from typing import Optional

from pydantic import BaseModel, conint, constr

"""
HTTP API Serializers
"""


class PostRequestSer(BaseModel):
    clientKey: str


class GetRequestSer(BaseModel):
    clientKey: str


class CaptchaOptionsSer(BaseModel):
    api_key: constr(min_length=36, max_length=36)
    sleep_time: conint(ge=5) = 5


"""
HTTP API Response
"""


class ResponseSer(BaseModel):
    balance: Optional[float] = 0
    # error info
    errorId: bool = False
    ErrorCode: Optional[str] = None
    errorDescription: Optional[str] = None
