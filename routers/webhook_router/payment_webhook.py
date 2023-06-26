from Crypto.Hash import SHA1
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings
from exceptions.BadRequest import BadRequest
from models.BillingAccountModel import BillingAccountModel
from models.TransactionModel import TransactionModel
from schemas.TransactionSchema import TransactionSchemaWebhook
from services.async_database import get_db

router = APIRouter()


@router.post('/payment/webhook/')
async def payment_webhook(
        data: TransactionSchemaWebhook,
        response: Response,
        db: AsyncSession = Depends(get_db)
) -> dict:
    signature = SHA1.new()
    signature.update(
        ':'.join((
            settings.PAYMENT_SECRET_KEY,
            str(data.transaction_id),
            str(data.user_id),
            str(data.bill_id),
            str(data.amount),
        )).encode()
    )

    expected_signature = signature.hexdigest()

    if not (expected_signature == data.signature):
        raise BadRequest(**{
            'detail': 'Not valid signature.',
        })

    try:
        billing_account = await BillingAccountModel.get_or_create(**{
            'user_id': data.user_id,
            'billing_account_id': data.bill_id,
            'db': db,
        })
    except IntegrityError:
        raise BadRequest(**{
            'detail': 'Not valid bill_id.',
        })

    await BillingAccountModel.update_balance(**{
        'billing_account_id': billing_account.id,
        'change_balance': data.amount,
        'db': db,
    })

    await TransactionModel.create(**{
        'data': data,
        'db': db,
    })

    response.status_code = status.HTTP_200_OK
    return {}
