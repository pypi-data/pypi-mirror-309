from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dynaconf import Dynaconf
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel
from src.core.standards.logger import logger

# from src.config.settings import settings


class DatabaseError(Exception):
    """数据库错误基类"""


class MySQLClient:
    """MySQL客户端实现 (单例模式)"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 初始化实例属性
            cls._instance._engine = None
            cls._instance._session_maker = None
        return cls._instance

    def get_engine(self) -> AsyncEngine:
        """获取数据库引擎"""
        if not self._engine:
            raise DatabaseError("Database engine not initialized")
        return self._engine

    async def initialize(self, settings: Dynaconf) -> None:
        """初始化数据库连接"""
        # 如果已经初始化过，直接返回
        if self._engine is not None:
            return
        try:
            self._engine = create_async_engine(
                url=settings.database.mysql_url,
                echo=settings.database.mysql_echo,
                pool_size=settings.database.mysql_pool_size,
                max_overflow=settings.database.mysql_max_overflow,
                pool_pre_ping=True,
                pool_recycle=3600,
            )

            self._session_maker = async_sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )

            # 测试连接
            async with self._session_maker() as session:
                result = await session.execute(text("SELECT 1"))
                value = result.scalar()
                if value != 1:
                    raise DatabaseError("Database connection test failed")
                await session.commit()

            logger.bind(request_id="system").info(
                f"Database initialized, url: {settings.database.mysql_url}",
                extra={
                    "host": settings.database.mysql_host,
                    "database": settings.database.mysql_database,
                },
            )
        except Exception as e:
            logger.bind(request_id="system").error(
                f"Failed to initialize database: {e}"
            )
            raise DatabaseError(
                f"Database initialization failed: {e}, dburl: {settings.database.mysql_url}"
            )

    async def close(self) -> None:
        """关闭数据库连接"""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None
            logger.bind(request_id="system").info("Database connection closed")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话"""
        if not self._session_maker:
            raise DatabaseError("Session maker not initialized")

        async with self._session_maker() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                logger.bind(request_id="system").error(f"Database session error: {e}")
                raise DatabaseError(f"Database session error: {e}")

    async def create_tables(self) -> None:
        """创建数据库表"""
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.bind(request_id="system").info("Database tables created")

    async def drop_tables(self) -> None:
        """删除数据库表"""
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            logger.bind(request_id="system").info("Database tables dropped")


# 创建全局单例实例
db = MySQLClient()
