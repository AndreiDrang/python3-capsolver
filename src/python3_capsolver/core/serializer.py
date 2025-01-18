from enum import Enum
from typing import Any, Dict, Literal, Optional

from msgspec import Struct

from .enum import ResponseStatusEnm
from .const import APP_ID

__all__ = ("PostRequestSer", "TaskSer", "RequestCreateTaskSer", "CaptchaResponseSer", "RequestGetTaskResultSer")


class MyBaseModel(Struct):
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for f in self.__struct_fields__:
            if isinstance(getattr(self, f), Enum):
                result.update({f: getattr(self, f).value})
            else:
                result.update({f: getattr(self, f)})
        return result


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
