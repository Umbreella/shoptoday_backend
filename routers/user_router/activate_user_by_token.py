from fastapi import APIRouter, Depends, Request, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError
from sqlalchemy.ext.asyncio import AsyncSession

from models.UserModel import UserModel
from permissions.AllowAny import AllowAny
from schemas.UserSchema import UserActivated, UserSchemaStatus
from services.async_database import get_db

router = APIRouter()


@router.get('/activate/{token}/')
@AllowAny
async def activate_user_by_token(
        request: Request,
        token: str,
        db: AsyncSession = Depends(get_db)
) -> UserActivated:
    decoded_token = AuthJWT().get_raw_jwt(token)

    if decoded_token.get('type') != 'activate':
        raise JWTDecodeError(**{
            'status_code': status.HTTP_403_FORBIDDEN,
            'message': 'Not valid token type.',
        })

    user_id = decoded_token.get('sub')
    data = UserSchemaStatus(**{
        'is_active': True,
    })

    await UserModel.update_status_by_id(user_id, data, db)

    return UserActivated(**{
        'detail': 'User is activated.',
    })
