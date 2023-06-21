from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from models.ProductModel import ProductModel
from permissions.is_admin import is_admin
from schemas.ProductSchema import ProductSchemaIn, ProductSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(
        data: ProductSchemaIn,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
) -> ProductSchemaOut:
    await is_admin(auth, db)

    product = await ProductModel.create(data, db)

    return product
