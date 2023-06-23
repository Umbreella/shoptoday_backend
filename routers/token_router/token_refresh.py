from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.ext.asyncio import AsyncSession

from models.BlackListToken import BlackListToken
from permissions.AllowAny import AllowAny
from schemas.TokenSchema import BothTokenSchema, RefreshTokenSchema
from services.async_database import get_db

router = APIRouter()


@router.post('/token/refresh/')
@AllowAny
async def token_refresh(
        request: Request,
        data: RefreshTokenSchema,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
) -> BothTokenSchema:
    try:
        payload = auth._verified_token(data.refresh)
    except AuthJWTException as ex:
        raise HTTPException(**{
            'detail': ex.message,
            'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        })

    if payload.get('type') != 'refresh':
        raise HTTPException(**{
            'detail': 'Invalid token type.',
            'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        })

    jti = payload.get('jti')

    is_blocked = await BlackListToken.check_token_by_jti(jti, db)

    if is_blocked:
        raise HTTPException(**{
            'detail': 'The token has already been used.',
            'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        })

    exp = payload.get('exp')
    await BlackListToken.add_in_black_list(jti, exp, db)

    subject = payload.get('sub')

    return BothTokenSchema(**{
        'access': auth.create_access_token(subject=subject),
        'refresh': auth.create_refresh_token(subject=subject),
    })
