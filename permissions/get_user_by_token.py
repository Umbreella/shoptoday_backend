from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.PermissionDenied import PermissionDenied
from models.UserModel import UserModel


async def get_user_by_token(auth: AuthJWT, db: AsyncSession) -> UserModel:
    auth.jwt_required()
    username = auth.get_jwt_subject()

    user = await UserModel.get_by_username(username, db)

    if not user:
        raise PermissionDenied()

    return user
