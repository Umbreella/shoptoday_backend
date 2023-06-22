from fastapi import Request
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from models.UserModel import UserModel


async def get_user_by_token(request: Request, db: AsyncSession) -> UserModel:
    auth = AuthJWT(request)

    auth.jwt_required()
    username = auth.get_jwt_subject()

    return await UserModel.get_by_username(username, db)
