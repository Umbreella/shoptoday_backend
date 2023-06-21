from fastapi import APIRouter

from . import (create_product, delete_product, list_products, retrieve_product,
               update_product)

router = APIRouter()

router.include_router(list_products.router)
router.include_router(create_product.router)
router.include_router(retrieve_product.router)
router.include_router(update_product.router)
router.include_router(delete_product.router)
