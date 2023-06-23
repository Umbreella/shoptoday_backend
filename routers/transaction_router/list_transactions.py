from fastapi import APIRouter, Depends, Request
from fastapi_pagination.cursor import CursorPage as Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.BadRequest import BadRequest
from exceptions.PermissionDenied import PermissionDenied
from models.BillingAccountModel import BillingAccountModel
from models.TransactionModel import TransactionModel
from permissions.IsAuthenticated import IsAuthenticated
from schemas.TransactionSchema import TransactionSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.get('/')
@IsAuthenticated
async def list_transactions(
        request: Request,
        billing_account: int | None = None,
        db: AsyncSession = Depends(get_db),
) -> Page[TransactionSchemaOut]:
    auth_user = request.jwt_user

    if not auth_user.is_superuser:
        if not billing_account:
            raise BadRequest(**{
                'detail': 'Missing query_params "billing_account".',
            })
        else:
            is_owner = await BillingAccountModel.check_owner(**{
                'user_id': auth_user.id,
                'billing_account_id': billing_account,
                'db': db,
            })

            if not is_owner:
                raise PermissionDenied()

    transactions = await TransactionModel.get_all_query(billing_account)

    return await paginate(db, transactions)
