from typing import List, Optional

from pydantic import Field, BaseModel, conint, constr

from python3_captchaai.core.enums import CaptchaTypeEnm

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
Captcha types serializers
"""


class ImageToTextTaskTask(TaskSer):
    body: str = Field(..., description="Base64 encoded content of the image (no line breaks)")


"""
HTTP API Response ser
"""


class ResponseSer(BaseModel):
    errorId: bool = Field(False, description="Error message: `False` - no error, `True` - with error")
    # error info
    ErrorCode: Optional[str] = Field(None, description="Error code")
    errorDescription: Optional[str] = Field(None, description="Error description")


class CreateTaskResponseSer(ResponseSer):
    taskId: Optional[str] = Field(None, description="Task ID for future use in getTaskResult method.")


class ControlResponseSer(ResponseSer):
    balance: Optional[float] = Field(0, description="Account balance value in USD")
    packages: List = Field(None, description="Monthly Packages")


"""
Other ser
"""


class CaptchaOptionsSer(BaseModel):
    api_key: constr(min_length=36, max_length=36)
    sleep_time: conint(ge=5) = 5
