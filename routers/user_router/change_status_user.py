from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.NotFound import NotFound
from models.UserModel import UserModel
from permissions.is_admin import is_admin
from schemas.UserSchema import UserSchemaOut, UserSchemaStatus
from services.async_database import get_db

router = APIRouter()


@router.patch('/{user_id}/')
async def change_status_user(
        user_id: int,
        data: UserSchemaStatus,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
) -> UserSchemaOut:
    await is_admin(auth, db)

    user = await UserModel.update_by_id(user_id, data, db)

    if not user:
        raise NotFound()

    return user
