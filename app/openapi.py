from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


class OpenapiSchema:
    def __init__(self, app: FastAPI):
        self._app = app

    def __call__(self, *args, **kwargs):
        openapi_schema = get_openapi(
            title='Shoptoday',
            version='v1',
            description=(
                'Add header \'Authorization: Bearer {access_token}\''
            ),
            routes=self._app.routes,
        )

        self._app.openapi_schema = openapi_schema

        return self._app.openapi_schema
