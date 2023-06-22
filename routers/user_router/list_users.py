from fastapi import APIRouter, Depends, Request
from fastapi_pagination.cursor import CursorPage as Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from models.UserModel import UserModel
from permissions.IsAdmin import IsAdmin
from schemas.UserSchema import UserSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.get('/')
@IsAdmin
async def list_users(
        request: Request,
        db: AsyncSession = Depends(get_db),
) -> Page[UserSchemaOut]:
    query = await UserModel.get_all_query()

    return await paginate(db, query)
