"""
业务逻辑层 - User
"""

# 导入引发的报错在创建项目之后会自动消失
import json
from typing import Any

from loguru import logger

from app.initializer import g
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.logging_fastcrud import LoggingFastCRUD


class UserService:
    """User 业务服务类"""

    def __init__(self) -> None:
        self.crud = LoggingFastCRUD(User)
        self.cache = getattr(g, "cache_manager", None)
        self.cache_prefix = "user:"

    def _cache_key(self, suffix: str) -> str:
        return f"{self.cache_prefix}{suffix}"

    async def list(
        self,
        page: int = 1,
        size: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        """获取User列表"""
        cache_key = self._cache_key(
            f"list:{page}:{size}:{json.dumps(filters or {}, sort_keys=True, ensure_ascii=False)}"
        )
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached:
                return cached  # type: ignore[return-value]

        async with g.db_async_session() as session:  # type: ignore[attr-defined]
            items, total = await self.crud.list(
                session=session,
                page=page,
                size=size,
                filter_by=filters or {},
            )

        result = (items, total)
        if self.cache:
            self.cache.set(cache_key, result, expire=300)
        return result

    async def get(self, id: str) -> dict[str, Any] | None:
        """获取单个User"""
        cache_key = self._cache_key(f"get:{id}")
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached:
                return cached  # type: ignore[return-value]

        async with g.db_async_session() as session:  # type: ignore[attr-defined]
            item = await self.crud.get(session=session, id=id)

        if item and self.cache:
            self.cache.set(cache_key, item, expire=300)
        return item

    async def create(self, data: UserCreate) -> str:
        """创建User"""
        async with g.db_async_session() as session:  # type: ignore[attr-defined]
            new_id = g.snow_client.generate_id_str()  # type: ignore[attr-defined]
            create_data = data.model_dump()
            create_data["id"] = new_id

            await self.crud.create(session=session, data=create_data)
            logger.info(f"创建User成功: {new_id}")
            return new_id

    async def update(self, id: str, data: UserUpdate) -> bool:
        """更新User"""
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_data:
            return True

        async with g.db_async_session() as session:  # type: ignore[attr-defined]
            updated = await self.crud.update(session=session, id=id, data=update_data)
            if updated:
                logger.info(f"更新User成功: {id}")
            return updated

    async def delete(self, id: str) -> bool:
        """删除User"""
        async with g.db_async_session() as session:  # type: ignore[attr-defined]
            deleted = await self.crud.delete(session=session, id=id)
            if deleted:
                logger.info(f"删除User成功: {id}")
            return deleted
