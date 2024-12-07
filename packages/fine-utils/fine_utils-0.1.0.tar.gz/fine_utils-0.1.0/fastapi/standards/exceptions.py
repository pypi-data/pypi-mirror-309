from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.standards.logger import logger
from fine_utils.fastapi.standards.response import ResponseUtil


class AppException(Exception):
    """应用基础异常"""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        category: str = "GENERAL",
        status_code: int = 500,
        context: dict | None = None,
    ):
        self.message = message
        self.code = code
        self.category = category
        self.status_code = status_code
        self.context = context or {}
        super().__init__(message)


# API 相关异常
class APIException(AppException):
    """API相关异常基类"""

    def __init__(self, message: str, code: str = "API_ERROR", status_code: int = 400):
        super().__init__(message, code, "API", status_code)


class RateLimitException(APIException):
    """API限流异常"""

    def __init__(self, message: str = "Too many requests"):
        super().__init__(message, "RATE_LIMIT", status_code=429)


class InvalidParameterException(APIException):
    """参数验证异常"""

    def __init__(self, message: str = "Invalid parameters"):
        super().__init__(message, "INVALID_PARAMS", status_code=400)


class UnauthorizedException(APIException):
    """未授权异常"""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, "UNAUTHORIZED", status_code=401)


class ForbiddenException(APIException):
    """禁止访问异常"""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message, "FORBIDDEN", status_code=403)


# 数据库相关异常
class DatabaseException(AppException):
    """数据库异常基类"""

    def __init__(self, message: str, code: str = "DB_ERROR"):
        super().__init__(message, code, "DATABASE", status_code=500)


class DatabaseConnectionException(DatabaseException):
    """数据库连接异常"""

    def __init__(self, message: str = "Database connection failed"):
        super().__init__(message, "DB_CONNECTION_ERROR")


class DatabaseQueryException(DatabaseException):
    """数据库查询异常"""

    def __init__(self, message: str = "Database query failed"):
        super().__init__(message, "DB_QUERY_ERROR")


class DatabaseIntegrityException(DatabaseException):
    """数据完整性异常"""

    def __init__(self, message: str = "Database integrity error"):
        super().__init__(message, "DB_INTEGRITY_ERROR")


# 缓存相关异常
class CacheException(AppException):
    """缓存异常基类"""

    def __init__(self, message: str, code: str = "CACHE_ERROR"):
        super().__init__(message, code, "CACHE", status_code=500)


class CacheConnectionException(CacheException):
    """缓存连接异常"""

    def __init__(self, message: str = "Cache connection failed"):
        super().__init__(message, "CACHE_CONNECTION_ERROR")


class CacheOperationException(CacheException):
    """缓存操作异常"""

    def __init__(self, message: str = "Cache operation failed"):
        super().__init__(message, "CACHE_OPERATION_ERROR")


# 业务相关异常
class BusinessException(AppException):
    """业务异常基类"""

    def __init__(self, message: str, code: str = "BUSINESS_ERROR"):
        super().__init__(message, code, "BUSINESS", status_code=400)


class ResourceNotFoundException(BusinessException):
    """资源不存在异常"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "RESOURCE_NOT_FOUND", status_code=404)


class ResourceConflictException(BusinessException):
    """资源冲突异常"""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, "RESOURCE_CONFLICT", status_code=409)


class BusinessValidationException(BusinessException):
    """业务验证异常"""

    def __init__(self, message: str = "Business validation failed"):
        super().__init__(message, "BUSINESS_VALIDATION_ERROR")


# 第三方服务相关异常
class ThirdPartyServiceException(AppException):
    """第三方服务异常基类"""

    def __init__(self, message: str, code: str = "THIRD_PARTY_ERROR"):
        super().__init__(message, code, "THIRD_PARTY", status_code=502)


class ThirdPartyRequestException(ThirdPartyServiceException):
    """第三方请求异常"""

    def __init__(self, message: str = "Third party request failed"):
        super().__init__(message, "THIRD_PARTY_REQUEST_ERROR")


class ThirdPartyResponseException(ThirdPartyServiceException):
    """第三方响应异常"""

    def __init__(self, message: str = "Third party response error"):
        super().__init__(message, "THIRD_PARTY_RESPONSE_ERROR")


# AI相关异常
class AIException(AppException):
    """AI相关异常基类"""

    def __init__(self, message: str, code: str = "AI_ERROR"):
        super().__init__(message, code, "AI", status_code=500)


class ModelNotFoundException(AIException):
    """模型不存在异常"""

    def __init__(self, message: str = "AI model not found"):
        super().__init__(message, "MODEL_NOT_FOUND")


class ModelInferenceException(AIException):
    """模型推理异常"""

    def __init__(self, message: str = "Model inference failed"):
        super().__init__(message, "MODEL_INFERENCE_ERROR")


class ExceptionHandlers:
    """全局异常处理器"""

    @staticmethod
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """处理HTTP异常"""
        logger.exception(f"HTTP exception: {exc}")
        return ResponseUtil.error(
            message=str(exc.detail), code="HTTP_ERROR", status_code=exc.status_code
        )

    @staticmethod
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """处理请求验证异常"""
        logger.exception("Validation error", extra={"errors": exc.errors()})
        return ResponseUtil.error(
            message="Request validation failed",
            code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            context={"errors": exc.errors()},
        )

    @staticmethod
    async def app_exception_handler(request: Request, exc: AppException):
        """处理应用异常"""
        logger.exception(f"Application exception: {exc}")
        return ResponseUtil.error(
            message=exc.message,
            code=exc.code,
            status_code=exc.status_code,
            context=exc.context,
        )

    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception):
        """处理未知异常"""
        logger.exception(f"Unhandled exception: {exc}")
        return ResponseUtil.error(
            message="Internal server error", code="INTERNAL_ERROR", status_code=500
        )


# 更新中间件配置
def get_exception_handlers():
    """获取异常处理器映射"""
    return {
        StarletteHTTPException: ExceptionHandlers.http_exception_handler,
        RequestValidationError: ExceptionHandlers.validation_exception_handler,
        AppException: ExceptionHandlers.app_exception_handler,
        Exception: ExceptionHandlers.general_exception_handler,
    }
