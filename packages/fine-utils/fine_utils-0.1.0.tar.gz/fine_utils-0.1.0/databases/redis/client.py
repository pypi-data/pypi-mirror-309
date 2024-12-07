from fine_redis import RedisClient, create_redis_client
from dynaconf import Dynaconf

# 创建全局Redis客户端实例
redis_client = create_redis_client()

async def initialize_redis(settings: Dynaconf) -> None:
    """初始化Redis连接"""
    # 从settings中提取Redis相关配置
    config = {
        "host": settings.database.redis_host,
        "port": settings.database.redis_port,
        "password": settings.database.redis_password,
        "database": settings.database.redis_db,
        "prefix": settings.database.redis_prefix,
        "tls": getattr(settings.database, "redis_tls", False),
        "cluster_mode": getattr(settings.database, "redis_cluster_mode", False),
    }
    await redis_client.initialize(config)
