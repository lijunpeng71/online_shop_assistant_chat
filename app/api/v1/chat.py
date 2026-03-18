from fastapi import APIRouter, Depends
from app.api.responses import Responses
from app.api.status import Status
from app.schemas.chat import ChatBase
from app.schemas.user import UserCreate, UserUpdate
from app.services.chat import ChatService
from app.services.user import UserService

router = APIRouter(prefix="/chat")
_active = True
_tag = "chat"


@router.post("")
async def chat(payload: ChatBase) -> dict:
    service = ChatService()
    return Responses.success(data={payload.message})
