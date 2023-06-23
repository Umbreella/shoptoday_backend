from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.ext.asyncio import AsyncSession

from permissions.AllowAny import AllowAny
from schemas.TokenSchema import AccessTokenSchema, RefreshTokenSchema
from services.async_database import get_db

router = APIRouter()


@router.post('/token/access/')
@AllowAny
async def token_refresh(
        request: Request,
        data: RefreshTokenSchema,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
) -> AccessTokenSchema:
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

    subject = payload.get('sub')

    return AccessTokenSchema(**{
        'access': auth.create_access_token(subject=subject),
    })
