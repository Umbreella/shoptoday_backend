from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.NotFound import NotFound
from models.UserModel import UserModel
from schemas.UserSchema import UserSchemaStatus
from services.async_database import get_db

router = APIRouter()


@router.get('/activate/{token}/')
async def activate_user_by_token(
        token: str,
        auth: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    decoded_token = auth.get_raw_jwt(token)

    user_id = decoded_token.get('sub')
    data = UserSchemaStatus(**{
        'is_active': True,
    })

    user = await UserModel.update_by_id(user_id, data, db)

    if not user:
        raise NotFound()

    return JSONResponse(**{
        'status_code': status.HTTP_200_OK,
        'content': {
            'detail': 'User is activated.',
        },
    })
