from fastapi import APIRouter, Depends
from fastapi_pagination.cursor import CursorPage as Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from models.ProductModel import ProductModel
from schemas.ProductSchema import ProductSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.get('/')
async def list_products(
        db: AsyncSession = Depends(get_db),
) -> Page[ProductSchemaOut]:
    query = await ProductModel.get_all_query()

    return await paginate(db, query)
