from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.NotFound import NotFound
from models.ProductModel import ProductModel
from permissions.AllowAny import AllowAny
from permissions.IsAdmin import IsAdmin
from schemas.ProductSchema import ProductSchemaIn, ProductSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.get('/{product_id}/')
@AllowAny
async def retrieve_product(
        request: Request,
        product_id: int,
        db: AsyncSession = Depends(get_db),
) -> ProductSchemaOut:
    product = await ProductModel.get_by_id(product_id, db)

    if not product:
        raise NotFound()

    return product


@router.put('/{product_id}/')
@IsAdmin
async def update_product(
        request: Request,
        product_id: int,
        data: ProductSchemaIn,
        db: AsyncSession = Depends(get_db),
) -> ProductSchemaOut:
    product = await ProductModel.update(product_id, data, db)

    if not product:
        raise NotFound()

    return product


@router.delete('/{product_id}/', status_code=status.HTTP_204_NO_CONTENT)
@IsAdmin
async def delete_product(
        request: Request,
        product_id: int,
        db: AsyncSession = Depends(get_db),
):
    product = await ProductModel.delete(product_id, db)

    if not product:
        raise NotFound()

    return product
