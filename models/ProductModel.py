from sqlalchemy import TEXT, Column, Integer, String

from services.database import BASE


class ProductModel(BASE):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(TEXT, nullable=False)
