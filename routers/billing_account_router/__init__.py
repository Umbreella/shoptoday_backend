from fastapi import APIRouter

from . import list_billing_account

router = APIRouter()

router.include_router(list_billing_account.router)
