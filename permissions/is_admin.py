from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.PermissionDenied import PermissionDenied
from models.UserModel import UserModel
from permissions.get_user_by_token import get_user_by_token


async def is_admin(auth: AuthJWT, db: AsyncSession) -> UserModel:
    user = await get_user_by_token(auth, db)

    if not user.is_superuser:
        raise PermissionDenied()

    return user
