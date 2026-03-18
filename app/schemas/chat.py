from pydantic import BaseModel, Field


class ChatBase(BaseModel):
    """chat 基础模式"""
    message: str = Field(..., min_length=1, max_length=100, description="名称")
