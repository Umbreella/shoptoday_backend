from sqlalchemy import (DECIMAL, TEXT, Column, Integer, String, delete, select,
                        update)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.ProductSchema import ProductSchemaIn
from services.async_database import BASE


class ProductModel(BASE):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(TEXT, nullable=False)
    price = Column(DECIMAL, default=0, nullable=False)

    @classmethod
    async def get_all_query(cls):
        return select(cls).order_by(cls.id)

    @classmethod
    async def get_by_id(cls, product_id: int, db: AsyncSession):
        query = select(cls).where(
            cls.id == product_id
        )

        rows = await db.execute(query)

        return rows.scalars().first()

    @classmethod
    async def create(cls, data: ProductSchemaIn, db: AsyncSession):
        query = insert(cls).values(
            data.dict()
        ).returning(cls)

        rows = await db.execute(query)

        return rows.scalars().first()

    @classmethod
    async def update(cls, product_id: int, data: ProductSchemaIn,
                     db: AsyncSession):
        query = update(cls).where(
            cls.id == product_id
        ).values(
            **data.dict()
        ).returning(cls)

        rows = await db.execute(query)

        return rows.scalars().first()

    @classmethod
    async def delete(cls, product_id: int, db: AsyncSession):
        query = delete(cls).where(
            cls.id == product_id
        ).returning(cls.id)

        rows = await db.execute(query)

        return rows.scalars().first()
