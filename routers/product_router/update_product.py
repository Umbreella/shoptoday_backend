from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.NotFound import NotFound
from models.ProductModel import ProductModel
from permissions.is_admin import is_admin
from schemas.ProductSchema import ProductSchemaIn, ProductSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.put('/{product_id}/')
async def update_product(
        product_id: int,
        data: ProductSchemaIn,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
) -> ProductSchemaOut:
    await is_admin(auth, db)

    product = await ProductModel.update(product_id, data, db)

    if not product:
        raise NotFound()

    return product
