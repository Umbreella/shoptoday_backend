from functools import wraps

from fastapi import Request


def AllowAny(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request')

        assert isinstance(request, Request), 'Missing kwargs "request".'

        request.jwt_user = None
        kwargs.update({
            'request': request,
        })

        return await func(*args, **kwargs)

    return wrapper
