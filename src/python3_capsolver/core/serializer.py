from typing import Any, Dict, Literal, Optional

from msgspec import Struct

from .enum import ResponseStatusEnm
from .const import APP_ID

__all__ = ("PostRequestSer", "TaskSer", "RequestCreateTaskSer", "CaptchaResponseSer")


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
