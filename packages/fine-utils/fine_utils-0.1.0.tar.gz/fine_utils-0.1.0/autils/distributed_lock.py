import uuid

from redis.asyncio import Redis

from src.core.standards.logger import logger


class DistributedLock:
    """分布式锁实现（异步版本）"""

    def __init__(
        self,
        redis: Redis,
        key: str,
        expire: int = 10,
        retry_delay: float = 0.1,
        retry_times: int = 50,
        blocking: bool = True,
    ):
        """
        初始化分布式锁

        Args:
            redis: Redis异步客户端实例
            key: 锁的键名
            expire: 锁的过期时间（秒）
            retry_delay: 重试等待时间（秒）
            retry_times: 重试次数
            blocking: 是否阻塞等待
        """
        self.redis = redis
        self.key = f"lock:{key}"
        self.expire = expire
        self.retry_delay = retry_delay
        self.retry_times = retry_times if blocking else 1
        self._lock_value = str(uuid.uuid4())  # 使用UUID作为锁的值
        self._locked = False

    async def __aenter__(self):
        """异步上下文管理器入口"""
        acquired = await self._acquire()
        if not acquired:
            raise Exception(f"Failed to acquire lock: {self.key}")
        return acquired

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self._locked:
            await self._release()
            self._locked = False

    async def _acquire(self) -> bool:
        """
        尝试获取锁

        Returns:
            bool: 是否成功获取锁
        """
        import asyncio

        for attempt in range(self.retry_times):
            try:
                # 使用 SET NX 原子操作设置锁
                success = await self.redis.set(
                    self.key, self._lock_value, ex=self.expire, nx=True
                )

                if success:
                    self._locked = True
                    logger.debug(
                        f"Acquired lock: {self.key} (value: {self._lock_value})"
                    )
                    return True

                if attempt < self.retry_times - 1:
                    await asyncio.sleep(self.retry_delay)
                    logger.debug(
                        f"Retrying to acquire lock: {self.key} (attempt {attempt + 1}/{self.retry_times})"
                    )

            except Exception as e:
                logger.error(f"Error acquiring lock: {self.key} - {e!s}")
                raise

        logger.warning(
            f"Failed to acquire lock after {self.retry_times} attempts: {self.key}"
        )
        return False

    async def _release(self) -> bool:
        """
        释放锁

        Returns:
            bool: 是否成功释放锁
        """
        # Lua脚本确保原子性操作
        lua_script = """
        if redis.call('get', KEYS[1]) == ARGV[1] then
            return redis.call('del', KEYS[1])
        else
            return 0
        end
        """

        try:
            # 执行Lua脚本
            result = await self.redis.eval(
                lua_script,
                1,  # key的数量
                self.key,  # KEYS[1]
                self._lock_value,  # ARGV[1]
            )

            success = bool(result)
            if success:
                logger.debug(f"Released lock: {self.key} (value: {self._lock_value})")
            else:
                logger.warning(
                    f"Failed to release lock: {self.key} "
                    f"(lock not owned or already expired)"
                )
            return success

        except Exception as e:
            logger.error(f"Error releasing lock: {self.key} - {e!s}")
            return False

    async def extend(self, additional_time: int) -> bool:
        """
        延长锁的过期时间

        Args:
            additional_time: 要增加的秒数

        Returns:
            bool: 是否成功延长
        """
        if not self._locked:
            return False

        try:
            # Lua脚本确保原子性操作
            lua_script = """
            if redis.call('get', KEYS[1]) == ARGV[1] then
                return redis.call('expire', KEYS[1], ARGV[2])
            else
                return 0
            end
            """

            result = await self.redis.eval(
                lua_script, 1, self.key, self._lock_value, str(additional_time)
            )

            success = bool(result)
            if success:
                logger.debug(f"Extended lock: {self.key} by {additional_time} seconds")
            else:
                logger.warning(f"Failed to extend lock: {self.key}")
            return success

        except Exception as e:
            logger.error(f"Error extending lock: {self.key} - {e!s}")
            return False

    async def is_locked(self) -> bool:
        """
        检查锁是否仍然有效

        Returns:
            bool: 锁是否有效
        """
        try:
            value = await self.redis.get(self.key)
            return value is not None and value.decode() == self._lock_value
        except Exception as e:
            logger.error(f"Error checking lock status: {self.key} - {e!s}")
            return False


"""
1. 基本使用：

async def update_config(config_id: int, new_value: dict):
    # 更新配置
    async with DistributedLock(redis_client, f"config_lock:{config_id}") as locked:
        if locked:
            config = await SystemConfig.get(config_id)
            config.value = new_value
            await config.save()

2. 带超时控制：

async def update_config_with_timeout(config_id: int, new_value: dict):
    # 带超时控制的更新配置
    import asyncio
    from contextlib import AsyncExitStack

    async with AsyncExitStack() as stack:
        try:
            # 设置超时
            await asyncio.wait_for(
                stack.enter_async_context(
                    DistributedLock(
                        redis_client,
                        f"config_lock:{config_id}",
                        expire=30
                    )
                ),
                timeout=5.0  # 5秒超时
            )

            # 执行更新操作
            config = await SystemConfig.get(config_id)
            config.value = new_value
            await config.save()

        except asyncio.TimeoutError:
            logger.error(f"Timeout acquiring lock for config {config_id}")
            raise

3. 自动延长锁时间：

async def long_running_operation():
    # 长时间运行的操作
    import asyncio

    lock = DistributedLock(redis_client, "long_operation_lock", expire=30)

    async def extend_lock():
        while True:
            await asyncio.sleep(20)  # 每20秒延长一次
            if not await lock.extend(30):
                break

    async with lock:
        # 启动自动延长任务
        extend_task = asyncio.create_task(extend_lock())
        try:
            # 执行长时间操作
            await some_long_operation()
        finally:
            # 取消延长任务
            extend_task.cancel()

4. 错误处理：

async def safe_update_config(config_id: int, new_value: dict):
    # 安全的配置更新
    lock = DistributedLock(
        redis_client,
        f"config_lock:{config_id}",
        retry_times=5,
        retry_delay=0.5
    )

    try:
        async with lock:
            config = await SystemConfig.get(config_id)
            if not config:
                raise ValueError(f"Config {config_id} not found")

            config.value = new_value
            await config.save()

    except Exception as e:
        logger.error(f"Failed to update config {config_id}: {str(e)}")
        raise

"""
