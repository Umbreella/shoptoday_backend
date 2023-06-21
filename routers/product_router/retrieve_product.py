from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.NotFound import NotFound
from models.ProductModel import ProductModel
from schemas.ProductSchema import ProductSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.get('/{product_id}/')
async def retrieve_product(
        product_id: int,
        db: AsyncSession = Depends(get_db),
) -> ProductSchemaOut:
    product = await ProductModel.get_by_id(product_id, db)

    if not product:
        raise NotFound()

    return product
