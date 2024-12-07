import asyncio
import json
import os
import sys
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import Any, TypeVar

import aiofiles

from src.core.standards.logger import logger

"""
主要改进：
1. 类型系统改进：
    TypeVar('T') 用于泛型编程，确保类型安全
    Callable[..., T] 表示一个返回类型为 T 的可调用对象
    添加了完整的类型注解
2. 功能增强：
    添加了共享线程池，避免频繁创建线程
    添加了文件写入功能
    增强了 JSON 文件处理功能
    添加了更多的参数选项
3. 错误处理：
    添加了详细的错误处理
    使用 logger 记录错误
    添加了自定义异常信息
4. 性能优化：
    使用共享线程池
    优化了文件操作
5. 文档完善：
    添加了详细的文档字符串
    添加了使用示例
    说明了参数类型和返回值
关于 TypeVar 和 Callable：
    TypeVar 用于泛型编程，它允许我们创建可以保持类型一致性的函数
    Callable 用于表示可调用对象（函数），[..., T] 表示接受任意参数并返回类型 T
例如：
T = TypeVar('T')
def process_data(func: Callable[..., T], data: Any) -> T:
    return func(data)

# 这样可以保证返回类型与函数返回类型一致
result_int = process_data(len, "hello")  # 返回 int
result_str = process_data(str.upper, "hello")  # 返回 str

"""

# T 是一个类型变量，用于泛型编程
# 它可以在运行时保持类型的一致性，比如函数的返回值类型与输入类型相同
T = TypeVar("T")

# 创建一个共享的线程池
_thread_pool = ThreadPoolExecutor(max_workers=10)

# 兼容性函数，用于在不同 Python 版本中运行同步函数
if sys.version_info >= (3, 9):
    async_run_sync = asyncio.to_thread
else:

    async def async_run_sync(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """
        异步运行同步函数
        :param func: 同步函数 (Callable 表示这是一个可调用对象，[..., T] 表示接受任意参数并返回类型T)
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: 函数返回值，类型与输入函数的返回类型相同
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(_thread_pool, partial(func, *args, **kwargs))


def to_async(func: Callable[..., T]) -> Callable[..., T]:
    """
    将同步函数转换为异步函数的装饰器
    :param func: 要转换的同步函数
    :return: 转换后的异步函数

    使用示例:
    @to_async
    def my_sync_function(x: int) -> int:
        return x * 2
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        return await async_run_sync(func, *args, **kwargs)

    return wrapper


async def aread_file(
    file_path: str, encoding: str = "utf-8", errors: str = "strict"
) -> str:
    """
    异步读取文件
    :param file_path: 文件路径
    :param encoding: 文件编码
    :param errors: 错误处理方式
    :return: 文件内容
    :raises ValueError: 文件不存在时抛出
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    try:
        async with aiofiles.open(file_path, encoding=encoding, errors=errors) as f:
            return await f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise


async def awrite_file(
    file_path: str, content: str, encoding: str = "utf-8", mode: str = "w"
) -> None:
    """
    异步写入文件
    :param file_path: 文件路径
    :param content: 要写入的内容
    :param encoding: 文件编码
    :param mode: 写入模式
    """
    try:
        async with aiofiles.open(file_path, mode=mode, encoding=encoding) as f:
            await f.write(content)
    except Exception as e:
        logger.error(f"Failed to write file {file_path}: {e}")
        raise


async def aread_json_file(file_path: str, encoding: str = "utf-8") -> dict[str, Any]:
    """
    异步读取JSON文件
    :param file_path: 文件路径
    :param encoding: 文件编码
    :return: JSON解析后的字典
    :raises Exception: JSON解析失败时抛出
    """
    try:
        content = await aread_file(file_path, encoding=encoding)
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from file {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to read JSON file {file_path}: {e}")
        raise


async def awrite_json_file(
    file_path: str,
    data: dict[str, Any],
    encoding: str = "utf-8",
    indent: int | None = None,
    ensure_ascii: bool = False,
) -> None:
    """
    异步写入JSON文件
    :param file_path: 文件路径
    :param data: 要写入的数据
    :param encoding: 文件编码
    :param indent: JSON缩进
    :param ensure_ascii: 是否确保ASCII编码
    """
    try:
        content = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
        await awrite_file(file_path, content, encoding=encoding)
    except Exception as e:
        logger.error(f"Failed to write JSON file {file_path}: {e}")
        raise
