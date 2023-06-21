from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.NotFound import NotFound
from models.ProductModel import ProductModel
from permissions.is_admin import is_admin
from services.async_database import get_db

router = APIRouter()


@router.delete('/{product_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: int,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
):
    await is_admin(auth, db)

    product = await ProductModel.delete(product_id, db)

    if not product:
        raise NotFound()

    return product
