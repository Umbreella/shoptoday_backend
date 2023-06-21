from Crypto.Hash import SHA1
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.BillingAccountModel import BillingAccountModel
from schemas.TransactionSchema import TransactionSchemaIn
from services.async_database import get_db
from settings import settings

router = APIRouter()


@router.post('/payment/webhook/')
async def payment_webhook(
        data: TransactionSchemaIn,
        response: Response,
        db: AsyncSession = Depends(get_db)
) -> None:
    signature = SHA1.new()
    signature.update(
        ':'.join((
            settings.PAYMENT_SECRET_KEY,
            data.transaction_id,
            data.user_id,
            data.bill_id,
            data.amount,
        )).encode()
    )

    if not (signature.hexdigest() == data.signature):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None

    billing_account = await BillingAccountModel.get_or_create(**{
        'user_id': data.user_id,
        'billing_account_id': data.bill_id,
        'db': db,
    })

    if not billing_account:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None

    await BillingAccountModel.update_balance(**{
        'billing_account_id': billing_account.id,
        'change_balance': data.amount,
        'db': db,
    })

    response.status_code = status.HTTP_200_OK
    return None
