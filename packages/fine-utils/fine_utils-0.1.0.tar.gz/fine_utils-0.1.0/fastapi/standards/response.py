from typing import Any

from fastapi.responses import JSONResponse

from fine_utils.fastapi.standards.schemas import BaseResponse, ErrorDetail


class ResponseUtil:
    """响应工具类"""

    @staticmethod
    def success(
        data: Any = None, message: str | None = None, status_code: int = 200
    ) -> JSONResponse:
        """成功响应"""
        return JSONResponse(
            status_code=status_code,
            content=BaseResponse(success=True, data=data, message=message).model_dump(),
        )

    @staticmethod
    def error(
        message: str,
        code: str = "INTERNAL_ERROR",
        detail: str | None = None,
        status_code: int = 500,
        exc_info: Exception | None = None,
        context: dict[str, Any] | None = None,
    ) -> JSONResponse:
        """错误响应"""
        if exc_info:
            detail = f"{detail or ''}\nException: {exc_info!s}"

        error_detail = ErrorDetail(code=code, message=message, detail=detail)

        response_data = {"success": False, "error": error_detail.model_dump()}
        if context:
            response_data["context"] = context

        return JSONResponse(status_code=status_code, content=response_data)
