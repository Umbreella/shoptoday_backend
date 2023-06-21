from fastapi import HTTPException, status


class BadRequest(HTTPException):
    def __init__(self, detail: str | dict):
        super().__init__(**{
            'status_code': status.HTTP_400_BAD_REQUEST,
            'detail': detail,
        })
