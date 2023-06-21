from fastapi import APIRouter

from . import sign_in, sign_up

router = APIRouter()

router.include_router(sign_in.router)
router.include_router(sign_up.router)
