from fastapi import APIRouter

from . import sign_in, sign_up, token_access, token_refresh

router = APIRouter()

router.include_router(sign_in.router)
router.include_router(sign_up.router)
router.include_router(token_refresh.router)
router.include_router(token_access.router)
