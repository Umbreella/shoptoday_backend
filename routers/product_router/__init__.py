from fastapi import APIRouter

from . import list_products, retrieve_product

router = APIRouter()

router.include_router(list_products.router)
router.include_router(retrieve_product.router)
