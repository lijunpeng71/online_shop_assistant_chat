"""
数据模式 - User
用于请求/响应数据验证
"""

from datetime import datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """User 基础模式"""

    name: str = Field(..., min_length=1, max_length=100, description="名称")
    description: str | None = Field(None, max_length=500, description="描述")
    status: int | None = Field(1, ge=0, le=1, description="状态: 1-启用, 0-禁用")


class UserCreate(UserBase):
    """创建User请求模式"""

    pass


class UserUpdate(BaseModel):
    """更新User请求模式（所有字段可选）"""

    name: str | None = Field(None, min_length=1, max_length=100, description="名称")
    description: str | None = Field(None, max_length=500, description="描述")
    status: int | None = Field(None, ge=0, le=1, description="状态: 1-启用, 0-禁用")


class UserResponse(UserBase):
    """User响应模式"""

    id: str = Field(..., description="主键ID")
    created_at: datetime | None = Field(None, description="创建时间")
    updated_at: datetime | None = Field(None, description="更新时间")

    class Config:
        from_attributes: bool = True


class UserListResponse(BaseModel):
    """User列表响应模式"""

    items: list[UserResponse] = Field(
        default_factory=list, description="数据列表"
    )
    total: int = Field(..., description="总数")
