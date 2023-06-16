from sqlalchemy import Boolean, Column, Integer, String

from services.database import BASE


class UserModel(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
