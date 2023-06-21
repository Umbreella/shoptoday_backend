from fastapi import APIRouter

from . import payment_webhook

router = APIRouter()

router.include_router(payment_webhook.router)
