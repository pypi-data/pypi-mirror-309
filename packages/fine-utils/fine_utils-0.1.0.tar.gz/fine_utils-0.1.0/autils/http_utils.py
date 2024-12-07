import asyncio
from dataclasses import dataclass, field
from typing import Any, TypeVar
from urllib.parse import urljoin
import time

import httpx


from src.core.standards.logger import logger
from src.core.standards.logger import request_id as ctx_request_id

T = TypeVar("T", bound="AsyncHttpClient")


@dataclass
class RetryConfig:
    """重试配置"""

    max_retries: int = 3
    retry_delay: float = 1.0
    """
    @dataclass 时，对于可变类型（如 set）的默认值设置方式不正确。在 Python 的 dataclass 中，不允许直接使用可变类型作为默认值，而是需要使用 default_factory
    使用 field(default_factory=lambda: {408, 429, 500, 502, 503, 504}) 替代直接的集合
    这样修改后就不会出现可变默认值的错误。这是因为：
        dataclass 的默认值在类定义时就会创建
        可变对象会被所有实例共享
        使用 default_factory 可以确保每个实例都获得自己的新副本
    """
    retry_codes: set[int] = field(
        default_factory=lambda: {408, 429, 500, 502, 503, 504}
    )


class AsyncHttpClientError(Exception):
    """HTTP客户端异常"""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: httpx.Response | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AsyncHttpClient:
    """异步HTTP客户端基类"""

    BASE_URL: str = ""
    DEFAULT_TIMEOUT: float = 10.0
    DEFAULT_HEADERS: dict[str, str] = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    AUTH: httpx.Auth | None = None
    RETRY_CONFIG: RetryConfig = RetryConfig()

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float | None = None,
        headers: dict[str, str] | None = None,
        auth: httpx.Auth | None = None,
        retry_config: RetryConfig | None = None,
    ):
        """初始化客户端"""
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.headers = {**self.DEFAULT_HEADERS, **(headers or {})}
        self.auth = auth or self.AUTH
        self.retry_config = retry_config or self.RETRY_CONFIG
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "AsyncHttpClient":
        """异步上下文管理器入口"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """异步上下文管理器出口"""
        await self.close()

    async def initialize(self) -> None:
        """初始化HTTP客户端"""
        if not self._client:
            self._client = httpx.AsyncClient(
                timeout=self.timeout, headers=self.headers, auth=self.auth
            )

    async def close(self) -> None:
        """关闭HTTP客户端"""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _should_retry(
        self,
        attempt: int,
        response: httpx.Response | None = None,
        error: Exception | None = None,
    ) -> bool:
        """判断是否需要重试"""
        if attempt >= self.retry_config.max_retries:
            return False

        if response and response.status_code in self.retry_config.retry_codes:
            return True

        if isinstance(error, (httpx.ConnectError, httpx.TimeoutException)):
            return True

        return False

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
        **kwargs,
    ) -> httpx.Response:
        """发送HTTP请求"""
        if not self._client:
            await self.initialize()

        full_url = urljoin(self.base_url, url)
        request_headers = {**self.headers, **(headers or {})}

        current_request_id = ctx_request_id.get()
        log = logger.bind(request_id=current_request_id)

        # 记录请求开始时间
        start_time = time.time()

        request_body = json if json is not None else data
        log.info(
            f"HTTP Request: {method} {full_url}",
            extra={
                "request": {
                    "method": method,
                    "url": full_url,
                    "params": params,
                    "headers": request_headers,
                    "body": request_body,
                }
            },
        )

        for attempt in range(self.retry_config.max_retries):
            try:
                response = await self._client.request(
                    method=method,
                    url=full_url,
                    params=params,
                    json=json,
                    data=data,
                    headers=request_headers,
                    timeout=timeout or self.timeout,
                    **kwargs,
                )

                # 计算请求耗时
                elapsed_time = time.time() - start_time

                response_info = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": None,
                    "elapsed_time": f"{elapsed_time:.3f}s",  # 添加耗时信息
                }

                try:
                    response_info["body"] = response.json()
                except:
                    response_info["body"] = response.text

                if response.is_error:
                    log.error(
                        f"HTTP Response Failed: {method} {full_url} - Status: {response.status_code} - Time: {elapsed_time:.3f}s",
                        extra={
                            "request": {
                                "method": method,
                                "url": full_url,
                                "params": params,
                                "headers": request_headers,
                                "body": request_body,
                            },
                            "response": response_info,
                        },
                    )
                    if await self._should_retry(attempt, response=response):
                        await asyncio.sleep(self.retry_config.retry_delay)
                        continue
                    response.raise_for_status()
                else:
                    log.info(
                        f"HTTP Response Success: {method} {full_url} - Status: {response.status_code} - Time: {elapsed_time:.3f}s",
                        extra={
                            "request": {
                                "method": method,
                                "url": full_url,
                                "params": params,
                                "headers": request_headers,
                                "body": request_body,
                            },
                            "response": response_info,
                        },
                    )

                return response

            except Exception as e:
                # 计算请求耗时（即使发生异常）
                elapsed_time = time.time() - start_time

                error_response = getattr(e, "response", None)
                error_info = {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "response": None,
                    "elapsed_time": f"{elapsed_time:.3f}s",  # 添加耗时信息
                }

                if error_response:
                    try:
                        error_info["response"] = {
                            "status_code": error_response.status_code,
                            "headers": dict(error_response.headers),
                            "body": error_response.json()
                            if error_response.headers.get("content-type")
                            == "application/json"
                            else error_response.text,
                        }
                    except:
                        error_info["response"] = {
                            "status_code": error_response.status_code,
                            "headers": dict(error_response.headers),
                            "body": error_response.text,
                        }
                try:
                    log.error(
                        f"HTTP Request Failed: {method} {full_url}, body: {error_response.text}",
                        # extra={
                        #     "request": {
                        #         "method": method,
                        #         "url": full_url,
                        #         "params": params,
                        #         "headers": request_headers,
                        #         "body": request_body,
                        #     },
                        #     "error": error_info,
                        # },
                    )
                except:
                    log.error(
                        f"failed HTTP Request Failed: {method} {full_url}, body: {error_response}",
                        # extra={
                        #     "request": {
                        #         "method": method,
                        #         "url": full_url,
                        #         "params": params,
                        #         "headers": request_headers,
                        #         "body": request_body,
                        #     },
                        #     "error": error_info,
                        # },
                    )

                if await self._should_retry(attempt, error=e):
                    await asyncio.sleep(self.retry_config.retry_delay)
                    continue
                raise AsyncHttpClientError(
                    f"Request failed: {e!s}",
                    status_code=getattr(e, "status_code", None),
                    response=getattr(e, "response", None),
                )

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """发送GET请求"""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        """发送POST请求"""
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> httpx.Response:
        """发送PUT请求"""
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> httpx.Response:
        """发送DELETE请求"""
        return await self.request("DELETE", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> httpx.Response:
        """发送PATCH请求"""
        return await self.request("PATCH", url, **kwargs)

    @classmethod
    async def create(cls: type[T], **kwargs) -> T:
        """创建客户端实例"""
        client = cls(**kwargs)
        await client.initialize()
        return client


async def temp_test():
    """
    工单加上展示UID信息
    """
    from src.config.settings import settings

    client = AsyncHttpClient(
        base_url=settings.zendesk.api_host,
        auth=httpx.BasicAuth(
            f"{settings.zendesk.api_email}/token", settings.zendesk.api_token
        ),
        headers={"User-Agent": "CustomClient/1.0", "Accept": "application/json"},
        timeout=60.0,
    )
    # r = await client.put(
    #     "/api/v2/tickets/32",
    #     json={
    #         "ticket": {
    #             "status": "closed",
    #         }
    #     },
    # )
    r = await client.get(
        "/api/v2/organizations",
    )
    # r = await client.get(
    #     "/api/v2/tickets.json",
    # )

    # orgid: 12929459397020
    # groupid: 12929459395740
    # r = await client.get(
    #     "/api/v2/organizations/12929459397020/users",
    # )

    # r = await client.get(
    #     "/api/v2/groups/16765533515676/users",
    # )
    # r = await client.get(
    #     "/api/v2/agent_availabilities/agent_statuses",
    # )

    # r = await client.put(
    #     "/api/v2/agent_availabilities/agent_statuses/agents/16765840571292",
    #     json={
    #         "id": 4,
    #     }
    # )
    # r = await client.get(
    #     "/api/v2/search.json",
    #     params={
    #         'query': 'type:ticket status:open type:user "hhczy1003@163.com"',
    #         'sort_by': 'created_at',
    #         'sort_order': 'desc'
    #     }
    # )

    # r = await client.get(
    #     "/api/v2/help_center/articles"
    # )
    print(r.text)
    # print(r.json()["ticket"]["description"])

async def refresh_ticket_new():
    from src.config.settings import settings

    client = AsyncHttpClient(
        base_url=settings.zendesk.api_host,
        auth=httpx.BasicAuth(
            f"{settings.zendesk.api_email}/token", settings.zendesk.api_token
        ),
        headers={"User-Agent": "CustomClient/1.0", "Accept": "application/json"},
        timeout=60.0,
    )
    while True:
        r = await client.get(
            "/api/v2/search.json",
            params={
                'query': 'type:ticket status:open',
                'sort_by': 'created_at',
                'sort_order': 'desc'
            }
        )
        content = r.json()
        for line in content["results"]:
            ticket_id = line["id"]
            status = line["status"]
            assignee_id = line["assignee_id"]
            print(f"{ticket_id}, {status}, {assignee_id}")
        await asyncio.sleep(1)
        # print(r.text)


if __name__ == "__main__":
    asyncio.run(temp_test())
    # asyncio.run(refresh_ticket_new())
