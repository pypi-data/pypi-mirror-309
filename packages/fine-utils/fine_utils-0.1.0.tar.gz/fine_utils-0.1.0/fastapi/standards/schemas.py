from typing import Generic, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class ErrorDetail(BaseModel):
    """错误详情"""

    code: str = Field(..., description="错误代码")
    message: str = Field(..., description="错误信息")
    detail: str | None = Field(None, description="详细错误信息")


class ErrorResponse(BaseModel):
    """错误响应"""

    success: bool = Field(False, description="是否成功")
    error: ErrorDetail = Field(..., description="错误信息")


class BaseResponse(BaseModel, Generic[DataT]):
    """基础响应模型"""

    success: bool = Field(True, description="是否成功")
    data: DataT | None = Field(None, description="响应数据")
    message: str | None = Field(None, description="响应消息")
