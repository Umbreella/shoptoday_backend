from sqlalchemy import Boolean, Column, Integer, String, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.UserSchema import UserSchemaIn, UserSchemaStatus
from services.async_database import BASE
from services.security import security


class UserModel(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)

    @classmethod
    async def authenticate(cls, data: UserSchemaIn, db: AsyncSession):
        query = select(UserModel).where(
            UserModel.username == data.username
        )

        rows = await db.execute(query)
        user = rows.scalars().first()

        if not user:
            return None

        if not user.is_active:
            return None

        if not security.verify_password(data.password, user.password):
            return None

        return user

    @classmethod
    async def get_all_query(cls):
        query = select(cls)

        return query.order_by(cls.id)

    @classmethod
    async def create(cls, data: UserSchemaIn, db: AsyncSession) -> str:
        query = insert(cls).values({
            'username': data.username,
            'password': security.get_password_hash(data.password),
        }).on_conflict_do_nothing().returning(cls)

        rows = await db.execute(query)

        return rows.scalars().first()

    @classmethod
    async def update_status_by_id(cls, user_id: int, data: UserSchemaStatus,
                                  db: AsyncSession):
        query = update(cls).where(
            cls.id == user_id
        ).values(
            **data.dict()
        ).returning(cls)

        rows = await db.execute(query)

        return rows.scalars().first()

    @classmethod
    async def get_by_username(cls, username: str, db: AsyncSession):
        query = select(cls).where(
            cls.username == username
        )

        rows = await db.execute(query)

        return rows.scalars().first()
