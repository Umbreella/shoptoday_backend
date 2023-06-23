from sqlalchemy import UUID, Column, Integer, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from services.async_database import BASE


class BlackListToken(BASE):
    __tablename__ = 'black_list_token'

    id = Column(Integer, primary_key=True)
    jti = Column(UUID(as_uuid=True), index=True, unique=True)
    exp = Column(Integer)

    @classmethod
    async def check_token_by_jti(cls, jti: str, db: AsyncSession) -> bool:
        select_query = select(cls).where(
            cls.jti == jti
        )

        select_rows = await db.execute(select_query)

        return bool(select_rows.scalars().first())

    @classmethod
    async def add_in_black_list(cls, jti: str, exp: int,
                                db: AsyncSession) -> bool:
        insert_query = insert(cls).values({
            'jti': jti,
            'exp': exp,
        }).on_conflict_do_nothing().returning(cls)

        insert_rows = await db.execute(insert_query)

        return bool(insert_rows.scalars().first())
