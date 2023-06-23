from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from models.UserModel import UserModel
from permissions.AllowAny import AllowAny
from schemas.TokenSchema import BothTokenSchema
from schemas.UserSchema import UserSchemaIn
from services.async_database import get_db

router = APIRouter()


@router.post('/sign_in/')
@AllowAny
async def sign_in(
        request: Request,
        data: UserSchemaIn,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db),
) -> BothTokenSchema:
    user = await UserModel.authenticate(data, db)

    if not user:
        raise HTTPException(**{
            'detail': 'User not found.',
            'status_code': status.HTTP_401_UNAUTHORIZED,
        })

    return BothTokenSchema(**{
        'access': auth.create_access_token(subject=user.username),
        'refresh': auth.create_refresh_token(subject=user.username),
    })
