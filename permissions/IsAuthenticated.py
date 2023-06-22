from functools import wraps

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.PermissionDenied import PermissionDenied

from .get_user_by_token import get_user_by_token


def IsAuthenticated(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request')
        db = kwargs.get('db')

        assert isinstance(request, Request), 'Missing kwargs \'request\'.'
        assert isinstance(db, AsyncSession), 'Missing kwargs \'db\'.'

        user = await get_user_by_token(request, db)

        if not user:
            raise PermissionDenied()

        request.jwt_user = user
        kwargs.update({
            'request': request,
        })

        return await func(*args, **kwargs)

    return wrapper
