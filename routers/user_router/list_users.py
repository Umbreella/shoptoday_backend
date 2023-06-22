from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination.cursor import CursorPage as Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from models.UserModel import UserModel
from permissions.is_admin import is_admin
from schemas.UserSchema import UserSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.get('/')
async def list_users(
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
) -> Page[UserSchemaOut]:
    await is_admin(auth, db)

    query = await UserModel.get_all_query()

    return await paginate(db, query)
