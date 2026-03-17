"""统一路由接口 - RESTful 模式

提供一组通用 RESTful 入口（可选启用，受白名单控制）：
- GET    /<resource>
- GET    /<resource>/{id}
- POST   /<resource>
- PATCH  /<resource>/{id}
- DELETE /<resource>/{id}

说明：
- 该路由通过资源名动态导入 service/schema 做分发。
- 若项目已为资源生成了显式模块路由（app.api.v1.<resource>），优先使用显式路由。
"""

import importlib
import re
from typing import Any

from fastapi import APIRouter
from app.initializer._settings import settings

router = APIRouter()

# 允许的资源白名单（安全机制）
# 从配置加载，留空则统一路由不可用
ALLOWED_RESOURCES: set[str] = set(settings.api_allowed_resources)
ALLOW_ALL: bool = settings.unified_route_allow_all
REQUIRE_AUTH: bool = True  # 始终强制认证

# 资源名称正则验证（只允许小写字母、数字和下划线）
RESOURCE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def _validate_resource(resource: str) -> bool:
    """
    验证资源名称是否合法

    Args:
        resource: 资源名称

    Returns:
        是否合法
    """
    # 检查命名格式
    if not RESOURCE_NAME_PATTERN.match(resource):
        return False

    # 如果设置了白名单，检查是否在白名单中
    if not ALLOW_ALL and ALLOWED_RESOURCES and resource not in ALLOWED_RESOURCES:
        return False

    return True


def _snake_to_pascal(name: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in name.split("_") if part)


def _get_service_instance(resource: str) -> Any | None:
    try:
        module_name = f"app.services.{resource}"
        service_module = importlib.import_module(module_name)
        service_class = getattr(service_module, f"{_snake_to_pascal(resource)}Service", None)
        if not service_class:
            return None
        return service_class()
    except Exception:
        return None


def _get_schema_types(resource: str) -> tuple[type[Any] | None, type[Any] | None]:
    try:
        module_name = f"app.schemas.{resource}"
        schema_module = importlib.import_module(module_name)
        pascal = _snake_to_pascal(resource)
        create_type = getattr(schema_module, f"{pascal}Create", None)
        update_type = getattr(schema_module, f"{pascal}Update", None)
        return create_type, update_type
    except Exception:
        return None, None
