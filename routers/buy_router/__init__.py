from fastapi import APIRouter

from . import create_buy_product

router = APIRouter()

router.include_router(create_buy_product.router)
