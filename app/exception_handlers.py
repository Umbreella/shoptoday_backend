from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException

from exceptions.handlers.JWTExceptionHandler import jwt_decode_error


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(AuthJWTException, jwt_decode_error)

    return app
