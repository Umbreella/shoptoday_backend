from fastapi import APIRouter, Depends, Request
from fastapi_pagination.cursor import CursorPage as Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession as ASession

from models.BillingAccountModel import BillingAccountModel
from permissions.IsAuthenticated import IsAuthenticated
from schemas.BillingAccountSchema import BillingAccountSchema
from services.async_database import get_db

router = APIRouter()


@router.get('/')
@IsAuthenticated
async def list_billing_accounts(
        request: Request,
        user: int | None = None,
        db: ASession = Depends(get_db),
) -> Page[BillingAccountSchema]:
    auth_user = request.jwt_user

    user_id = user if auth_user.is_superuser else auth_user.id

    bank_accounts = await BillingAccountModel.get_all_query(**{
        'user_id': user_id,
    })

    return await paginate(db, bank_accounts)
