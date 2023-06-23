from fastapi import APIRouter, Depends, Request, status
from fastapi_pagination.cursor import CursorPage as Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from models.ProductModel import ProductModel
from permissions.AllowAny import AllowAny
from permissions.IsAdmin import IsAdmin
from schemas.ProductSchema import ProductSchemaIn, ProductSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.get('/')
@AllowAny
async def list_products(
        request: Request,
        db: AsyncSession = Depends(get_db),
) -> Page[ProductSchemaOut]:
    query = await ProductModel.get_all_query()

    return await paginate(db, query)


@router.post('/', status_code=status.HTTP_201_CREATED)
@IsAdmin
async def create_product(
        request: Request,
        data: ProductSchemaIn,
        db: AsyncSession = Depends(get_db),
) -> ProductSchemaOut:
    product = await ProductModel.create(data, db)

    return product
