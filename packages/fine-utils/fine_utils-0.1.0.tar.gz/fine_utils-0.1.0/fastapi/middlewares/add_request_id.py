import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from fine_logger import ContextLogger, request_id


class RequestIdMiddleware(BaseHTTPMiddleware):
    """请求ID中间件"""

    async def dispatch(self, request: Request, call_next):
        # 从请求头获取请求ID，如果没有则生成新的
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # 设置请求ID到上下文
        request_id.set(req_id)
        # 兼容旧代码
        ContextLogger.set_request_id(req_id)

        try:
            response = await call_next(request)
            # 在响应头中添加请求ID
            response.headers["X-Request-ID"] = req_id
            return response
        finally:
            # 清理上下文
            request_id.set("system")
            ContextLogger.clear_context()
