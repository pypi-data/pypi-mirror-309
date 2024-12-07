from datetime import UTC, datetime
from enum import IntEnum
from typing import Any, Optional, TypeVar
from zoneinfo import ZoneInfo

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
from sqlmodel import Field, SQLModel, asc, desc, select

from fine_utils.databases.mysql import db
from src.core.standards.logger import logger

T = TypeVar("T", bound="BaseDBModel")


class RecordStatus(IntEnum):
    """记录状态枚举"""

    ACTIVE = 1
    DELETED = 0


class BaseDBModel(SQLModel):
    """基础数据库模型"""

    id: int | None = Field(default=None, primary_key=True)
    status: RecordStatus = Field(
        default=RecordStatus.ACTIVE,
        description="记录状态：1-有效 0-删除",
        index=True,  # 直接使用 index=True
    )

    # 创建信息
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="创建时间(UTC)",
        index=True,  # 直接使用 index=True
    )
    created_by: str | None = Field(default=None, description="创建人ID")

    # 更新信息
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="最后更新时间(UTC)",
        index=True,  # 直接使用 index=True
    )
    updated_by: str | None = Field(default=None, description="更新人ID")

    @classmethod
    def build_base_query(cls) -> Select:
        """构建基础查询（只查询有效数据）"""
        return select(cls).where(cls.status == RecordStatus.ACTIVE)

    # CRUD 操作
    @classmethod
    async def create(cls: type[T], *, obj_in: dict, created_by: str | None = None) -> T:
        """创建记录"""
        try:
            obj_in["created_by"] = created_by
            obj_in["updated_by"] = created_by
            db_obj = cls(**obj_in)

            async with db.get_session() as session:
                session.add(db_obj)
                await session.commit()
                await session.refresh(db_obj)
                return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Create {cls.__name__} failed: {e}")
            raise

    @classmethod
    async def get(cls: type[T], id: int) -> T | None:
        """获取单条记录"""
        try:
            async with db.get_session() as session:
                query = cls.build_base_query().where(cls.id == id)
                result = await session.exec(query)
                return result.first()
        except SQLAlchemyError as e:
            logger.error(f"Get {cls.__name__} failed: {e}")
            raise

    @classmethod
    async def get_multi(
        cls: type[T], *, skip: int = 0, limit: int = 100, filters: dict | None = None
    ) -> list[T]:
        """获取多条记录"""
        try:
            async with db.get_session() as session:
                query = cls.build_base_query()

                # 添加过滤条件
                if filters:
                    for field, value in filters.items():
                        if hasattr(cls, field):
                            query = query.where(getattr(cls, field) == value)

                query = query.offset(skip).limit(limit)
                result = await session.exec(query)
                return result.all()
        except SQLAlchemyError as e:
            logger.error(f"Get multi {cls.__name__} failed: {e}")
            raise

    async def update(self, *, obj_in: dict, updated_by: str | None = None) -> T:
        """更新记录"""
        try:
            obj_in["updated_by"] = updated_by
            obj_in["updated_at"] = datetime.now(UTC)

            for field, value in obj_in.items():
                if hasattr(self, field):
                    setattr(self, field, value)

            async with db.get_session() as session:
                session.add(self)
                await session.commit()
                await session.refresh(self)
                return self
        except SQLAlchemyError as e:
            logger.error(f"Update {self.__class__.__name__} failed: {e}")
            raise

    async def delete(self, deleted_by: str | None = None) -> bool:
        """软删除记录"""
        try:
            self.status = RecordStatus.DELETED
            self.updated_by = deleted_by
            self.updated_at = datetime.now(UTC)

            async with db.get_session() as session:
                session.add(self)
                await session.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Delete {self.__class__.__name__} failed: {e}")
            raise

    async def hard_delete(self) -> bool:
        """硬删除记录"""
        try:
            async with db.get_session() as session:
                await session.delete(self)
                await session.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Hard delete {self.__class__.__name__} failed: {e}")
            raise

    def get_local_time(self, dt: datetime, tz: str = "Asia/Shanghai") -> datetime:
        """获取本地时间"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(ZoneInfo(tz))

    @property
    def local_created_at(self) -> datetime:
        """本地创建时间"""
        return self.get_local_time(self.created_at)

    @property
    def local_updated_at(self) -> datetime:
        """本地更新时间"""
        return self.get_local_time(self.updated_at)

    def update_creator(self, user_id: str) -> None:
        """更新创建人ID"""
        self.created_by = user_id

    def update_modifier(self, user_id: str) -> None:
        """更新修改人ID"""
        self.updated_by = user_id

    @classmethod
    def build_query(
        cls,
        filters: dict[str, Any] | None = None,
        order_by: list[tuple[str, bool]] | None = None,
        joins: list[str] | None = None,
    ) -> Select:
        """构建查询语句"""
        # 创建基础查询（默认只查询有效数据）
        query = cls.build_base_query()

        # 合并额外的过滤条件
        if filters:
            for field, value in filters.items():
                if hasattr(cls, field):
                    if isinstance(value, (list, tuple)):
                        query = query.where(getattr(cls, field).in_(value))
                    elif isinstance(value, dict):
                        operator = value.get("operator", "eq")
                        val = value.get("value")
                        if operator == "like":
                            query = query.where(getattr(cls, field).like(f"%{val}%"))
                        elif operator == "gt":
                            query = query.where(getattr(cls, field) > val)
                        elif operator == "lt":
                            query = query.where(getattr(cls, field) < val)
                        elif operator == "between":
                            start, end = val
                            query = query.where(getattr(cls, field).between(start, end))
                    else:
                        query = query.where(getattr(cls, field) == value)

        # 添加排序
        if order_by:
            for field, is_desc in order_by:
                if hasattr(cls, field):
                    query = query.order_by(
                        desc(getattr(cls, field))
                        if is_desc
                        else asc(getattr(cls, field))
                    )

        # 添加关联
        if joins:
            for join in joins:
                if hasattr(cls, join):
                    query = query.options(selectinload(getattr(cls, join)))

        return query

    # @classmethod
    # async def search(
    #     cls: Type[T],
    #     *,
    #     filters: Dict[str, Any] | None = None,
    #     order_by: List[Tuple[str, bool]] | None = None,
    #     page: int = 1,
    #     page_size: int = 10,
    #     count_total: bool = True
    # ) -> Tuple[List[T], int]:
    #     """
    #     搜索记录
    #     :param filters: 过滤条件
    #     :param order_by: 排序条件，元组列表，每个元组包含字段名和是否升序
    #     :param page: 页码
    #     :param page_size: 每页数量
    #     :param count_total: 是否统计总数
    #     :return: (记录列表, 总数)
    #     """
    #     try:
    #         # 构建查询
    #         query = cls.build_query(filters)

    #         # 添加排序
    #         if order_by:
    #             for field, asc in order_by:
    #                 if hasattr(cls, field):
    #                     order_col = getattr(cls, field)
    #                     query = query.order_by(order_col if asc else desc(order_col))

    #         # 分页
    #         query = query.offset((page - 1) * page_size).limit(page_size)

    #         async with db.get_session() as session:
    #             # 执行查询
    #             result = await session.execute(query)
    #             items = result.scalars().all()

    #             # 统计总数
    #             total = 0
    #             if count_total:
    #                 count_query = select(func.count()).select_from(cls)
    #                 if filters:
    #                     for field, value in filters.items():
    #                         if hasattr(cls, field):
    #                             count_query = count_query.where(getattr(cls, field) == value)
    #                 count_result = await session.execute(count_query)
    #                 total = count_result.scalar() or 0

    #             return list(items), total

    #     except SQLAlchemyError as e:
    #         logger.error(f"Search {cls.__name__} failed: {e}")
    #         raise

    @classmethod
    async def search(
        cls: type[T],
        *,
        filters: dict[str, Any] | None = None,
        order_by: list[tuple[str, bool]] | None = None,
        skip: int = 0,
        limit: int | None = None,  # 修改为可选参数
        select_fields: list[str] | None = None,
        include_deleted: bool = False,
    ) -> tuple[list[T], int]:
        """
        高级搜索方法
        :param filters: 过滤条件，如 {"age": {"operator": "gt", "value": 18}}
        :param order_by: 排序条件，如 [("created_at", True)] True表示降序
        :param skip: 跳过记录数
        :param limit: 返回记录数限制，None表示返回所有记录
        :param select_fields: 要选择的字段列表
        :param include_deleted: 是否包含已删除记录
        :return: (记录列表, 总记录数)
        """
        try:
            async with db.get_session() as session:
                # 构建查询
                if select_fields:
                    query = select(*[getattr(cls, field) for field in select_fields])
                else:
                    query = select(cls)

                # 添加状态过滤
                if not include_deleted:
                    query = query.where(cls.status == RecordStatus.ACTIVE)

                # 添加其他过滤条件...（保持原有逻辑）

                # 计算总数
                count_query = select(func.count()).select_from(query.subquery())
                total = await session.scalar(count_query) or 0

                # 添加分页
                if skip:
                    query = query.offset(skip)
                if limit is not None:  # 只在明确指定limit时添加限制
                    query = query.limit(limit)

                result = await session.execute(query)
                return result.scalars().all(), total

        except SQLAlchemyError as e:
            logger.error(f"Search {cls.__name__} failed: {e}")
            raise

    @classmethod
    async def bulk_create(cls: type[T], objects: list[dict]) -> list[T]:
        """批量创建"""
        try:
            db_objects = [cls(**obj) for obj in objects]
            async with db.get_session() as session:
                session.add_all(db_objects)
                await session.commit()
                for obj in db_objects:
                    await session.refresh(obj)
                return db_objects
        except SQLAlchemyError as e:
            logger.error(f"Bulk create {cls.__name__} failed: {e}")
            raise

    @classmethod
    async def bulk_update(
        cls: type[T], filters: dict[str, Any], update_data: dict[str, Any]
    ) -> int:
        """批量更新"""
        try:
            query = cls.build_query(filters)
            async with db.get_session() as session:
                result = await session.exec(query.with_for_update())
                objects = result.all()

                for obj in objects:
                    for field, value in update_data.items():
                        if hasattr(obj, field):
                            setattr(obj, field, value)

                await session.commit()
                return len(objects)
        except SQLAlchemyError as e:
            logger.error(f"Bulk update {cls.__name__} failed: {e}")
            raise

    @classmethod
    async def get_latest(cls: type[T], order_by_field: str = "created_at") -> T | None:
        """
        获取最新记录
        :param order_by_field: 排序字段，默认创建时间
        """
        try:
            if not hasattr(cls, order_by_field):
                raise ValueError(f"Field {order_by_field} not found in {cls.__name__}")

            query = (
                cls.build_base_query()
                .order_by(desc(getattr(cls, order_by_field)))
                .limit(1)
            )

            async with db.get_session() as session:
                result = await session.exec(query)
                return result.first()
        except SQLAlchemyError as e:
            logger.error(f"Get latest {cls.__name__} failed: {e}")
            raise

    @classmethod
    async def get_max_id(cls: type[T]) -> int:
        """获取最大ID"""
        try:
            query = select(func.max(cls.id)).select_from(cls)
            async with db.get_session() as session:
                result = await session.execute(query)
                return result.scalar() or 0
        except SQLAlchemyError as e:
            logger.error(f"Get max id for {cls.__name__} failed: {e}")
            raise

    @classmethod
    async def update(cls: type[T], id: Any, **kwargs) -> T | None:
        """更新记录"""
        async with db.get_session() as session:
            query = select(cls).where(cls.id == id)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                instance.updated_at = datetime.utcnow()
                await session.commit()
                await session.refresh(instance)
            return instance

    @classmethod
    async def get(cls: type[T], id: Any) -> T | None:
        """获取记录"""
        async with db.get_session() as session:
            query = select(cls).where(cls.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_multi(
        cls: type[T],
        *,
        skip: int = 0,
        limit: int | None = 100,
        order_by: list[tuple[str, bool]] | None = None,
        joins: list[str] | None = None,
    ) -> list[T]:
        """获取多条记录"""
        try:
            async with db.get_session() as session:
                # 使用 build_base_query 获取基础查询（只包含活跃记录）
                query = cls.build_base_query()

                # 添加排序
                if order_by:
                    for field, is_desc in order_by:
                        if hasattr(cls, field):
                            query = query.order_by(
                                desc(getattr(cls, field))
                                if is_desc
                                else asc(getattr(cls, field))
                            )

                # 添加关联
                if joins:
                    for join in joins:
                        if hasattr(cls, join):
                            query = query.options(selectinload(getattr(cls, join)))

                # 添加分页
                if skip:
                    query = query.offset(skip)
                if limit is not None:
                    query = query.limit(limit)

                result = await session.execute(query)
                return result.scalars().all()  # 使用 scalars() 来获取结果

        except SQLAlchemyError as e:
            logger.error(f"Get multi {cls.__name__} failed: {e}")
            raise

    @classmethod
    async def all(
        cls: type[T],
        *,
        order_by: list[tuple[str, bool]] | None = None,
        joins: list[str] | None = None,
    ) -> list[T]:
        """
        获取所有活跃记录

        Args:
            order_by: 排序条件，格式为 [("field_name", is_desc)]，例如 [("created_at", True)] 表示按创建时间降序
            joins: 需要预加载的关联关系列表

        Returns:
            list[T]: 活跃记录列表
        """
        try:
            # 直接复用 get_multi 方法
            return await cls.get_multi(
                skip=0,
                limit=None,  # 不限制数量，获取所有记录
            )

        except SQLAlchemyError as e:
            logger.error(f"Get all {cls.__name__} records failed: {e}")
            raise

    @classmethod
    async def get_by_filters(cls, filters: dict) -> Optional["BaseDBModel"]:
        """根据过滤条件获取单个记录"""
        try:
            async with db.get_session() as session:
                query = select(cls).filter_by(**filters)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to get {cls.__name__} by filters: {e}")
            raise

    @classmethod
    async def get_by_key_and_env(
        cls, key: str, environment: str
    ) -> Optional["BaseDBModel"]:
        """根据键和环境获取记录"""
        filters = {
            "key": key,
            "environment": environment,
            "status": RecordStatus.ACTIVE,
        }
        return await cls.get_by_filters(filters)

    @classmethod
    async def delete(cls: type[T], id: Any) -> T | None:
        """删除记录"""
        async with db.get_session() as session:
            query = select(cls).where(cls.id == id)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance:
                await session.delete(instance)
                await session.commit()
            return instance

    async def save(self) -> "BaseDBModel":
        """保存记录（upsert 模式）"""
        async with db.get_session() as session:
            if self.id is None:
                # 创建新记录
                session.add(self)
                await session.commit()
                await session.refresh(self)
            else:
                # 更新现有记录
                self.updated_at = datetime.utcnow()
                query = select(self.__class__).where(self.__class__.id == self.id)
                result = await session.execute(query)
                instance = result.scalar_one_or_none()
                if instance:
                    # 更新现有实例的属性
                    for key, value in self.model_dump().items():
                        if key not in ["id", "created_at"]:
                            setattr(instance, key, value)
                    await session.commit()
                    # 更新当前实例
                    for key, value in instance.model_dump().items():
                        setattr(self, key, value)
                else:
                    # ID 不存在，创建新记录
                    session.add(self)
                    await session.commit()
                    await session.refresh(self)
            return self

    @classmethod
    async def count(cls: type[T], filters: dict[str, Any] | None = None) -> int:
        """
        计算符合条件的记录数量
        :param filters: 过滤条件，如 {"conversation_id": 123}
        :return: 记录数量
        """
        try:
            async with db.get_session() as session:
                # 构建基础查询（只查询有效数据）
                query = (
                    select(func.count())
                    .select_from(cls)
                    .where(cls.status == RecordStatus.ACTIVE)
                )

                # 添加过滤条件
                if filters:
                    for field, value in filters.items():
                        if hasattr(cls, field):
                            if isinstance(value, (list, tuple)):
                                query = query.where(getattr(cls, field).in_(value))
                            elif isinstance(value, dict):
                                operator = value.get("operator", "eq")
                                val = value.get("value")
                                if operator == "like":
                                    query = query.where(
                                        getattr(cls, field).like(f"%{val}%")
                                    )
                                elif operator == "gt":
                                    query = query.where(getattr(cls, field) > val)
                                elif operator == "lt":
                                    query = query.where(getattr(cls, field) < val)
                                elif operator == "between":
                                    start, end = val
                                    query = query.where(
                                        getattr(cls, field).between(start, end)
                                    )
                            else:
                                query = query.where(getattr(cls, field) == value)

                result = await session.execute(query)
                return result.scalar() or 0

        except SQLAlchemyError as e:
            logger.error(f"Count {cls.__name__} failed: {e}")
            raise


# 使用示例
class User(BaseDBModel, table=True):
    """用户模型"""

    __tablename__ = "users"

    name: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    age: int | None = Field(None, description="年龄")


# 使用示例
async def example_usage():
    # 高级搜索
    users, total = await User.search(
        filters={
            "age": {"operator": "gt", "value": 18},
            "name": {"operator": "like", "value": "john"},
        },
        order_by=[("created_at", True)],
        skip=0,
        limit=10,
    )

    # 批量创建
    new_users = await User.bulk_create(
        [
            {"name": "user1", "email": "user1@example.com"},
            {"name": "user2", "email": "user2@example.com"},
        ]
    )

    # 批量更新
    updated_count = await User.bulk_update(
        filters={"age": {"operator": "lt", "value": 18}},
        update_data={"status": RecordStatus.DELETED},
    )

    # 获取最新记录
    latest_user = await User.get_latest()

    # 获取最大ID
    max_id = await User.get_max_id()
