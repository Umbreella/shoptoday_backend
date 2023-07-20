from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.settings import settings


def add_middleware(app: FastAPI):
    app.add_middleware(**{
        'middleware_class': CORSMiddleware,
        'allow_credentials': True,
        'allow_origins': settings.FASTAPI_APP_ALLOW_ORIGINS.split(' '),
        'allow_methods': [
            'DELETE',
            'GET',
            'OPTIONS',
            'PATCH',
            'POST',
            'PUT',
        ],
        'allow_headers': [
            'accept',
            'accept-encoding',
            'access-control-allow-credentials',
            'access-control-expose-headers',
            'authorization',
            'content-type',
            'dnt',
            'origin',
            'user-agent',
            'x-requested-with',
        ],
    })

    return app
