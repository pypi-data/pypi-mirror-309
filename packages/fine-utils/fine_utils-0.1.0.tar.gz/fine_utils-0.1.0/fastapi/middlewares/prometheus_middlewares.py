import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from prometheus_client import Histogram, Counter

# 创建响应时间直方图
REQUEST_TIME = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint', 'status_code']
)

# 创建请求计数器
REQUEST_COUNT = Counter(
    'http_request_count_total',
    'Total HTTP request count',
    ['method', 'endpoint', 'status_code']
) 

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        # 计算请求处理时间
        duration = time.time() - start_time
        
        # 获取路由路径（如果没有路由，则使用原始路径）
        route = request.scope.get("route")
        endpoint = route.path if route else request.url.path
        
        # 记录请求时间
        REQUEST_TIME.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=response.status_code
        ).observe(duration)
        
        # 记录请求计数
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=response.status_code
        ).inc()
        
        return response
