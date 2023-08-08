from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.BadRequest import BadRequest
from models.BillingAccountModel import BillingAccountModel
from models.ProductModel import ProductModel
from permissions.IsAuthenticated import IsAuthenticated
from schemas.BuySchema import BuyProductSchema, BuyStatus
from services.async_database import get_db

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
@IsAuthenticated
async def create_buy_product(
        request: Request,
        data: BuyProductSchema,
        db: AsyncSession = Depends(get_db),
) -> BuyStatus:
    auth_user = request.jwt_user

    product = await ProductModel.get_by_id(data.product, db)

    if not product:
        raise BadRequest(**{
            'detail': {
                'product': 'Object does not exist.',
            },
        })

    is_owner = await BillingAccountModel.check_owner(**{
        'user_id': auth_user.id,
        'billing_account_id': data.billing_account,
        'db': db,
    })

    if not is_owner:
        raise BadRequest(**{
            'detail': {
                'billing_account': 'Object does not exist.',
            },
        })

    operation_status = await BillingAccountModel.update_balance(**{
        'billing_account_id': data.billing_account,
        'change_balance': float(-product.price),
        'db': db,
    })

    return BuyStatus(**{
        'status': operation_status,
    })
