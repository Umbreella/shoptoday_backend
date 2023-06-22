from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.NotFound import NotFound
from models.UserModel import UserModel
from permissions.IsAdmin import IsAdmin
from schemas.UserSchema import UserSchemaOut, UserSchemaStatus
from services.async_database import get_db

router = APIRouter()


@router.patch('/{user_id}/')
@IsAdmin
async def change_status_user(
        request: Request,
        user_id: int,
        data: UserSchemaStatus,
        db: AsyncSession = Depends(get_db),
) -> UserSchemaOut:
    user = await UserModel.update_by_id(user_id, data, db)

    if not user:
        raise NotFound()

    return user
