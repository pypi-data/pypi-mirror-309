from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from fine_utils.fastapi.standards.exceptions import ResponseUtil
from src.core.standards.logger import logger


class ExceptionMidlleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            logger.exception("Uncatched Exception")
            return ResponseUtil.error(
                message=str(e),
                code="HTTP_ERROR",
                # status_code=e.status_code
            )
