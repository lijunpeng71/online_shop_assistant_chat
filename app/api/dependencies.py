"""
API 依赖注入
提供 JWT 认证和 API Key 验证的依赖函数
"""

# 导入引发的报错在创建项目之后会自动消失
from fastapi import Depends, Header, HTTPException, status
from app.utils.api_key_util import is_valid_api_key


async def get_api_key(x_api_key: str | None = Header(None)) -> str | None:
    """
    从请求头获取API Key

    Args:
        x_api_key: X-API-Key请求头

    Returns:
        API Key字符串或None
    """
    return x_api_key


async def verify_api_key_required(api_key: str | None = Depends(get_api_key)) -> str:
    """
    验证API Key（必须）

    从配置中读取有效的 API Keys 列表进行验证。

    Args:
        api_key: API Key

    Returns:
        API Key字符串

    Raises:
        HTTPException: 如果API Key无效
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少API Key",
        )

    # 验证 API Key 是否在配置的有效列表中
    if not is_valid_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key无效",
        )

    return api_key


async def verify_api_key_optional(
    api_key: str | None = Depends(get_api_key),
) -> str | None:
    """
    验证API Key（可选）

    如果提供了 API Key，则验证其有效性。

    Args:
        api_key: API Key

    Returns:
        API Key字符串或None

    Raises:
        HTTPException: 如果提供的API Key无效
    """
    if not api_key:
        return None

    if not is_valid_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key无效",
        )

    return api_key
