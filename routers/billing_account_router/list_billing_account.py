from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination.cursor import CursorPage as Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession as ASession

from models.BillingAccountModel import BillingAccountModel
from permissions.get_user_by_token import get_user_by_token
from schemas.BankAccountSchema import BankAccountSchema
from services.async_database import get_db

router = APIRouter()


@router.get('/')
async def list_billing_accounts(
        user: int | None = None,
        auth: AuthJWT = Depends(),
        db: ASession = Depends(get_db),
) -> Page[BankAccountSchema]:
    auth_user = await get_user_by_token(auth, db)

    user_id = user if auth_user.is_superuser else auth_user.id

    bank_accounts = await BillingAccountModel.get_all_query(**{
        'user_id': user_id,
    })

    return await paginate(db, bank_accounts)
