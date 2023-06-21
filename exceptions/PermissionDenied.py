from fastapi import HTTPException, status


class PermissionDenied(HTTPException):
    def __init__(self):
        super().__init__(**{
            'status_code': status.HTTP_403_FORBIDDEN,
            'detail': 'You don`t have permission to access this resource.',
        })
