"""API接口 - User

RESTful 风格接口：
- GET    /user
- GET    /user/{id}
- POST   /user
- PATCH  /user/{id}
- DELETE /user/{id}
"""

from fastapi import APIRouter, Depends
from app.api.responses import Responses
from app.api.status import Status
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/user")
_active = True
_tag = "user"


@router.get("")
async def list_user(
    page: int = 1,
    size: int = 10,
) -> dict:
    service = UserService()
    items, total = await service.list(page=page, size=size)
    return Responses.success(data={"items": items, "total": total})


@router.get("/{id}")
async def get_user(
    id: str
) -> dict:
    service = UserService()
    data = await service.get(id)
    if not data:
        return Responses.failure(status=Status.RECORD_NOT_EXIST_ERROR)
    return Responses.success(data=data)


@router.post("")
async def create_user(
    payload: UserCreate
) -> dict:
    service = UserService()
    new_id = await service.create(payload)
    return Responses.success(data={"id": new_id})


@router.patch("/{id}")
async def update_user(
    id: str,
    payload: UserUpdate,
) -> dict:
    service = UserService()
    ok = await service.update(id, payload)
    if not ok:
        return Responses.failure(status=Status.RECORD_NOT_EXIST_ERROR)
    return Responses.success(data={"id": id})


@router.delete("/{id}")
async def delete_user(
    id: str
) -> dict:
    service = UserService()
    ok = await service.delete(id)
    if not ok:
        return Responses.failure(status=Status.RECORD_NOT_EXIST_ERROR)
    return Responses.success(data={"id": id})
