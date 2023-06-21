from fastapi import APIRouter

from . import activate_user_by_token, change_status_user, list_users

router = APIRouter()

router.include_router(activate_user_by_token.router)
router.include_router(change_status_user.router)
router.include_router(list_users.router)
