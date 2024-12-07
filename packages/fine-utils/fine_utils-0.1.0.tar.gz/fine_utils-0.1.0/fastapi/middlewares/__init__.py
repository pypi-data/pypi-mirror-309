"""基础中间件"""

from fastapi import FastAPI

# from src.settings import settings
from starlette.middleware.exceptions import ExceptionMiddleware

from fine_utils.fastapi.standards.exceptions import get_exception_handlers

from .add_request_id import RequestIdMiddleware
from .timing import TimingMiddleware
from .prometheus_middlewares import PrometheusMiddleware

def setup_middlewares(app: FastAPI) -> None:
    """设置所有中间件"""
    # 代理中间件
    # if settings.BEHIND_PROXY:
    #     app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
    #
    # 异常处理中间件
    app.add_middleware(ExceptionMiddleware, handlers=get_exception_handlers())

    # 基础中间件
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(PrometheusMiddleware)

