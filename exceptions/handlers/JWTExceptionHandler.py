from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


async def jwt_decode_error(request: Request, exc: HTTPException):
    return JSONResponse(**{
        'status_code': status.HTTP_403_FORBIDDEN,
        'content': {
            'detail': exc.message,
        },
    })
