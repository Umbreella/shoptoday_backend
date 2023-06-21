from fastapi import APIRouter

from . import list_transactions

router = APIRouter()

router.include_router(list_transactions.router)
