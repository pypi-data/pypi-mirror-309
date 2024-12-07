# ... existing imports ...
import time
from datetime import datetime
from typing import Optional, Set, Dict, Any, Coroutine
from weakref import WeakSet
from contextlib import contextmanager
import asyncio
from src.core.standards.logger import logger
# ... existing code ...

class AsyncTaskManager:
    """
    异步任务管理器
    - 管理异步任务的创建、执行和取消
    - 记录任务执行时间和状态
    - 提供错误处理和日志记录
    - 支持任务分组和批量操作
    """

    def __init__(self):
        # 使用 WeakSet 存储活动任务，避免内存泄漏
        self._active_tasks: WeakSet[asyncio.Task] = WeakSet()
        # 存储任务元数据
        self._task_meta: Dict[asyncio.Task, Dict[str, Any]] = {}
        # 任务分组
        self._task_groups: Dict[str, Set[asyncio.Task]] = {}

    async def create_task(
        self,
        coro: Coroutine,
        *,
        name: Optional[str] = None,
        group: Optional[str] = None,
        timeout: Optional[float] = None,
        retry_count: int = 0,
        retry_delay: float = 1.0,
        auto_start: bool = True,  # 新增参数：控制是否立即启动
    ) -> asyncio.Task:
        """
        创建并管理异步任务

        Args:
            coro: 要执行的协程
            name: 任务名称
            group: 任务组名称
            timeout: 任务超时时间（秒）
            retry_count: 失败重试次数
            retry_delay: 重试间隔时间（秒）
            auto_start: 是否立即启动任务，默认为True

        Returns:
            asyncio.Task: 创建的任务对象
        """

        async def _wrapped_coro():
            start_time = time.time()
            attempt = 0

            while True:
                try:
                    # 记录任务开始
                    logger.info(f"Task {name or 'unnamed'} started at {datetime.now()}")

                    # 使用 timeout 控制任务执行时间
                    if timeout:
                        result = await asyncio.wait_for(coro, timeout=timeout)
                    else:
                        result = await coro

                    # 记录任务成功完成
                    execution_time = time.time() - start_time
                    logger.info(
                        f"Task {name or 'unnamed'} completed successfully in {execution_time:.2f}s"
                    )
                    return result

                except asyncio.TimeoutError:
                    logger.error(f"Task {name or 'unnamed'} timed out after {timeout}s")
                    raise

                except asyncio.CancelledError:
                    execution_time = time.time() - start_time
                    logger.warning(
                        f"Task {name or 'unnamed'} was cancelled after {execution_time:.2f}s"
                    )
                    raise

                except Exception as e:
                    attempt += 1
                    execution_time = time.time() - start_time

                    if attempt <= retry_count:
                        logger.warning(
                            f"Task {name or 'unnamed'} failed (attempt {attempt}/{retry_count}): {str(e)}"
                            f"\nRetrying in {retry_delay}s..."
                        )
                        await asyncio.sleep(retry_delay)
                    else:
                        logger.exception(
                            f"Task {name or 'unnamed'} failed after {execution_time:.2f}s: {str(e)}",
                            exc_info=True
                        )
                        raise


        # 创建任务但不立即启动
        if not auto_start:
            # 在 Python 3.11+ 中可以使用 asyncio.create_task(..., start=False)
            # 为了兼容性，我们返回一个未启动的 Task
            task = asyncio.create_task(_wrapped_coro(), name=name)
            task.cancel()  # 立即取消，使任务进入未启动状态
        else:
            task = asyncio.create_task(_wrapped_coro(), name=name)

        # 存储任务元数据
        self._task_meta[task] = {
            "name": name,
            "group": group,
            "start_time": time.time(),
            "timeout": timeout,
        }

        # 添加到活动任务集合
        self._active_tasks.add(task)

        # 添加到任务组
        if group:
            if group not in self._task_groups:
                self._task_groups[group] = set()
            self._task_groups[group].add(task)

        # 添加任务完成回调
        task.add_done_callback(self._task_done_callback)

        return task

    def _task_done_callback(self, task: asyncio.Task) -> None:
        """任务完成回调处理"""
        # 清理任务元数据
        meta = self._task_meta.pop(task, {})
        group = meta.get("group")

        # 从任务组中移除
        if group and group in self._task_groups:
            self._task_groups[group].discard(task)
            if not self._task_groups[group]:
                del self._task_groups[group]

    def cancel_task(self, task: asyncio.Task) -> bool:
        """
        取消指定任务

        Returns:
            bool: 是否成功取消
        """
        if not task.done():
            task.cancel()
            return True
        return False

    def cancel_group(self, group: str) -> int:
        """
        取消指定组的所有任务

        Returns:
            int: 取消的任务数量
        """
        if group not in self._task_groups:
            return 0

        count = 0
        for task in self._task_groups[group].copy():
            if self.cancel_task(task):
                count += 1
        return count

    def cancel_all(self) -> int:
        """
        取消所有活动任务

        Returns:
            int: 取消的任务数量
        """
        count = 0
        for task in self._active_tasks.copy():
            if self.cancel_task(task):
                count += 1
        return count

    @contextmanager
    def task_group(self, group_name: str, *, auto_cancel: bool = False):
        """
        任务分组上下文管理器

        Args:
            group_name: 任务组名称
            auto_cancel: 退出时是否自动取消任务，默认为False

        Example:
            # 不自动取消任务
            async with task_manager.task_group("my_group") as group:
                task1 = await group.create_task(some_coro())
                task2 = await group.create_task(other_coro())

            # 自动取消任务
            async with task_manager.task_group("my_group", auto_cancel=True) as group:
                task1 = await group.create_task(some_coro())
        """
        class TaskGroup:
            def __init__(self, manager: 'AsyncTaskManager', group: str):
                self.manager = manager
                self.group = group

            async def create_task(self, coro: Coroutine, **kwargs):
                return await self.manager.create_task(
                    coro, group=self.group, **kwargs
                )

            def get_tasks(self) -> Set[asyncio.Task]:
                """获取组内所有任务"""
                return self.manager._task_groups.get(self.group, set()).copy()

        try:
            yield TaskGroup(self, group_name)
        finally:
            # 只在指定auto_cancel=True时才自动取消任务
            if auto_cancel:
                self.cancel_group(group_name)

    @property
    def active_tasks(self) -> Set[asyncio.Task]:
        """获取当前活动的任务集合"""
        return set(self._active_tasks)

    @property
    def task_groups(self) -> Dict[str, Set[asyncio.Task]]:
        """获取任务分组信息"""
        return self._task_groups.copy()


async_task_manager = AsyncTaskManager()
