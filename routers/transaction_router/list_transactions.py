from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.PermissionDenied import PermissionDenied
from models.BillingAccountModel import BillingAccountModel
from models.TransactionModel import TransactionModel
from permissions.get_user_by_token import get_user_by_token
from services.async_database import get_db

router = APIRouter()


@router.get('/')
async def list_transactions(
        billing_account: int | None = None,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
):
    auth_user = await get_user_by_token(auth, db)

    if not auth_user.is_superuser:
        is_owner = await BillingAccountModel.check_owner(**{
            'user_id': auth_user.id,
            'billing_account_id': billing_account,
            'db': db,
        })

        if not is_owner:
            raise PermissionDenied()

    transactions = await TransactionModel.get_all_query(**{
        'billing_account': billing_account,
        'db': db,
    })

    return await paginate(db, transactions)
