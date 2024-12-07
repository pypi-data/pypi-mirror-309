import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.standards.logger import logger


class TimingMiddleware(BaseHTTPMiddleware):
    """请求计时中间件"""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        path = request.url
        method = request.method

        async def timed_call_next(request: Request):
            try:
                response = await call_next(request)
            except Exception as e:
                # 让异常继续传播，但是在传播之前记录时间
                process_time = (time.time() - start_time) * 1000
                logger.info(
                    f"{method} {path} - Took {process_time:.2f}ms (with exception)"
                )
                # 这个很重要 避免重复传播异常链条
                raise e from None

            process_time = (time.time() - start_time) * 1000
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            logger.info(f"{method} {path} - Took {process_time:.2f}ms")
            return response

        return await timed_call_next(request)
