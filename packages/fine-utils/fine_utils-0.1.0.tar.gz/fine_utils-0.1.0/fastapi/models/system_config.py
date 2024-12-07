from datetime import datetime
from enum import Enum
from typing import Any, Optional

from sqlalchemy import Column, Integer, func, select, text
from sqlmodel import JSON, Field

from fine_utils.fastapi.models.base_model import BaseDBModel, RecordStatus
from fine_utils.databases.mysql import db
from fine_utils.databases.redis import redis_client
from src.core.standards.logger import logger
from fine_utils.autils.distributed_lock import DistributedLock


class ConfigValueType(str, Enum):
    """配置值类型"""

    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    JSON = "json"
    LIST = "list"
    DICT = "dict"


class ConfigEncryptionType(str, Enum):
    """配置加密类型"""

    NONE = "none"
    AES = "aes"
    RSA = "rsa"
    FERNET = "fernet"


class ConfigEnvironment(str, Enum):
    """配置环境"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class SystemConfig(BaseDBModel, table=True):
    """系统配置表"""

    __tablename__ = "system_configs"

    # 基础配置信息
    module: str = Field(..., max_length=50, description="配置模块", index=True)
    key: str = Field(..., max_length=100, description="配置键", index=True)
    value: Any = Field(..., sa_column=Column(JSON), description="配置值")
    value_type: ConfigValueType = Field(
        default=ConfigValueType.STRING, description="值类型"
    )

    # 环境和描述
    environment: ConfigEnvironment = Field(
        default=ConfigEnvironment.DEVELOPMENT, description="环境", index=True
    )
    description: str | None = Field(
        default=None, max_length=500, description="配置描述"
    )

    # 版本控制
    version: int = Field(
        sa_column=Column(
            Integer, nullable=False, server_default=text("1"), comment="配置版本号"
        )
    )
    is_deprecated: bool = Field(default=False, description="是否已废弃")

    # 加密配置
    encryption_type: ConfigEncryptionType = Field(
        default=ConfigEncryptionType.NONE, description="加密类型"
    )
    encryption_key_id: str | None = Field(
        default=None, max_length=100, description="加密密钥ID"
    )

    # 审计和控制
    last_modified_reason: str | None = Field(
        default=None, max_length=200, description="最后修改原因"
    )
    is_readonly: bool = Field(default=False, description="是否只读")
    requires_approval: bool = Field(default=False, description="是否需要审批")
    approved_by: str | None = Field(default=None, max_length=50, description="审批人")
    approved_at: datetime | None = Field(default=None, description="审批时间")

    class Config:
        """模型配置"""

        json_schema_extra = {
            "example": {
                "module": "database",
                "key": "database.url",
                "value": {"host": "localhost", "port": 5432},
                "value_type": "json",
                "environment": "development",
                "description": "数据库连接配置",
                "version": 1,
                "encryption_type": "none",
                "is_readonly": False,
                "requires_approval": True,
            }
        }

    # 自定义方法
    async def increment_version(self, reason: str | None = None) -> None:
        """增加版本号（使用分布式锁）"""
        lock_key = f"config_version:{self.module}:{self.key}:{self.environment}"

        async with DistributedLock(redis_client, lock_key, expire=10) as locked:
            if not locked:
                raise Exception("Failed to acquire lock for version increment")

            try:
                async with db.get_session() as session:
                    # 获取当前最大版本号
                    stmt = select(func.max(SystemConfig.version)).where(
                        SystemConfig.module == self.module,
                        SystemConfig.key == self.key,
                        SystemConfig.environment == self.environment,
                    )
                    result = await session.execute(stmt)
                    max_version = result.scalar() or 0

                    # 更新版本号和修改原因
                    self.version = max_version + 1
                    if reason:
                        self.last_modified_reason = reason

                    await session.commit()
                    logger.info(
                        f"Incremented version for {self.module}.{self.key} "
                        f"to {self.version} ({reason or 'no reason provided'})"
                    )
            except Exception as e:
                logger.error(f"Failed to increment version: {e}")
                raise

    async def update(
        self,
        *,
        obj_in: dict,
        updated_by: str | None = None,
        reason: str | None = None,
        skip_version_increment: bool = False,
    ) -> "SystemConfig":
        """更新配置"""
        # 检查只读状态
        if self.is_readonly:
            raise ValueError(f"Config {self.key} is readonly")

        # 检查是否需要审批
        if self.requires_approval and not obj_in.get("approved_by"):
            raise ValueError(f"Config {self.key} requires approval")

        # 如果值发生变化且不跳过版本递增，则增加版本号
        if (
            "value" in obj_in
            and obj_in["value"] != self.value
            and not skip_version_increment
        ):
            await self.increment_version(reason)

        return await super().update(obj_in=obj_in, updated_by=updated_by)

    @classmethod
    async def create_with_validation(
        cls, *, obj_in: dict, created_by: str | None = None
    ) -> "SystemConfig":
        """创建配置（带验证）"""
        # 检查是否已存在
        existing = await cls.get_by_key_and_env(
            key=obj_in["key"],
            environment=obj_in["environment"],
            module=obj_in["module"],
        )
        if existing:
            raise ValueError(f"Config {obj_in['key']} already exists")

        # 验证值类型
        value_type = obj_in.get("value_type", ConfigValueType.STRING)
        value = obj_in["value"]

        if value_type == ConfigValueType.NUMBER:
            if not isinstance(value, (int, float)):
                raise ValueError("Value must be a number")
        elif value_type == ConfigValueType.BOOLEAN:
            if not isinstance(value, bool):
                raise ValueError("Value must be a boolean")
        elif value_type == ConfigValueType.JSON:
            if not isinstance(value, dict):
                raise ValueError("Value must be a JSON object")
        elif value_type == ConfigValueType.LIST:
            if not isinstance(value, list):
                raise ValueError("Value must be a list")

        return await cls.create(obj_in=obj_in, created_by=created_by)

    @classmethod
    async def get_by_key_and_env(
        cls,
        key: str,
        environment: str = ConfigEnvironment.DEVELOPMENT,
        module: str | None = None,
    ) -> Optional["SystemConfig"]:
        """通过键名和环境获取配置"""
        filters = {
            "key": key,
            "environment": environment,
            "status": RecordStatus.ACTIVE,
            "module": module,
            "is_deprecated": False,
        }
        return await cls.get_by_filters(filters)

    async def get_version_history(self) -> list["SystemConfigHistory"]:
        """获取配置版本历史"""
        return await SystemConfigHistory.get_history(
            module=self.module, key=self.key, environment=self.environment
        )

    async def deprecate(self, *, reason: str, deprecated_by: str) -> None:
        """废弃配置"""
        await self.update(
            obj_in={
                "is_deprecated": True,
                "last_modified_reason": f"Deprecated: {reason}",
            },
            updated_by=deprecated_by,
            skip_version_increment=True,
        )

    @property
    def decrypted_value(self) -> Any:
        """获取解密后的值"""
        if self.encryption_type == ConfigEncryptionType.NONE:
            return self.value
        return self._decrypt_value()

    def _decrypt_value(self) -> Any:
        """解密值"""
        # 解密逻辑实现...


class SystemConfigHistory(BaseDBModel, table=True):
    """系统配置历史表"""

    __tablename__ = "system_config_history"

    config_id: int = Field(..., description="配置ID", index=True)
    module: str = Field(..., description="配置模块")
    key: str = Field(..., description="配置键")
    environment: str = Field(..., description="环境")
    value: Any = Field(..., sa_column=Column(JSON), description="配置值")
    version: int = Field(..., description="版本号")
    modified_by: str = Field(..., description="修改人")
    modified_reason: str | None = Field(default=None, description="修改原因")

    @classmethod
    async def get_history(
        cls, module: str, key: str, environment: str
    ) -> list["SystemConfigHistory"]:
        """获取配置历史记录"""
        filters = {"module": module, "key": key, "environment": environment}
        return await cls.search(filters=filters, order_by=[("version", True)])
