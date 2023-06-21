from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from models.UserModel import UserModel
from schemas.UserSchema import UserSchemaIn
from services.async_database import get_db

router = APIRouter()


@router.post('/sign_up/')
async def sign_up(
        request: Request,
        data: UserSchemaIn,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    user = await UserModel.create(data, db)

    if not user:
        raise HTTPException(**{
            'detail': 'This username is used.',
            'status_code': status.HTTP_400_BAD_REQUEST,
        })

    activate_token = auth._create_token(**{
        'subject': user.id,
        'exp_time': datetime.utcnow() + timedelta(days=1),
        'type_token': 'activate',
    })

    activate_url = request.url_for('activate_user_by_token',
                                   token=activate_token, )

    return JSONResponse(**{
        'status_code': status.HTTP_201_CREATED,
        'content': {
            'activate_url': str(activate_url),
        },
    })
