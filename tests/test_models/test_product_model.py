from decimal import Decimal

from sqlalchemy import select

from models.ProductModel import ProductModel
from schemas.ProductSchema import ProductSchemaIn, ProductSchemaOut
from services.async_database import async_database

tested_class = ProductModel
data = {
    'title': 'new_product',
    'description': 'new_product',
    'price': 10_000,
}


async def test_When_CallGetAllQuery_Should_SelectWithOrderBy():
    expected_query = str(
        select(
            tested_class
        ).order_by(
            tested_class.id
        ))
    real_query = str(await tested_class.get_all_query())

    assert expected_query == real_query


async def test_When_CallGetByIdWithNotFoundId_Should_ReturnNone():
    async with async_database.session() as db, db.begin():
        product_orm = await tested_class.get_by_id(1, db)

    expected_product = None
    real_product = product_orm

    assert expected_product == real_product


async def test_When_CallGetByIdWithFoundId_Should_ReturnProduct(
        filling_products,
):
    async with async_database.session() as db, db.begin():
        product_orm = await tested_class.get_by_id(1, db)
        product = ProductSchemaOut.from_orm(product_orm)

    expected_product = {
        'id': 1,
        'title': 'product',
        'description': 'product',
        'price': 1_000,
    }
    real_product = product.dict()

    assert expected_product == real_product


async def test_When_CallCreateProductModel_Should_ReturnProduct():
    local_data = ProductSchemaIn(**data)

    async with async_database.session() as db, db.begin():
        product_orm = await tested_class.create(local_data, db)
        product = ProductSchemaOut.from_orm(product_orm)

        select_rows = await db.execute(
            select(tested_class)
        )
        select_result = select_rows.scalars().all()

    expected_product = {
        'id': 1,
        'title': 'new_product',
        'description': 'new_product',
        'price': 10_000,
    }
    real_product = product.dict()

    expected_len_products = 1
    real_len_products = len(select_result)

    assert expected_product == real_product
    assert expected_len_products == real_len_products


async def test_When_CallUpdateProductWithNotFoundId_Should_ReturnNone():
    local_data = ProductSchemaIn(**data)

    async with async_database.session() as db, db.begin():
        product_orm = await tested_class.update(1, local_data, db)

    expected_product = None
    real_product = product_orm

    assert expected_product == real_product


async def test_When_CallUpdateProductWithFoundId_Should_ReturnNone(
        filling_products,
):
    local_data = ProductSchemaIn(**data)

    async with async_database.session() as db, db.begin():
        product_orm = await tested_class.update(1, local_data, db)
        product = ProductSchemaOut.from_orm(product_orm)

        select_rows = await db.execute(
            select(tested_class).where(tested_class.id == 1)
        )
        select_result = ProductSchemaOut.from_orm(
            select_rows.scalars().first()
        )

    expected_product = {
        'id': 1,
        'title': 'new_product',
        'description': 'new_product',
        'price': 10_000,
    }
    real_product = product.dict()

    expected_title = 'new_product'
    real_title = select_result.title

    expected_description = 'new_product'
    real_description = select_result.description

    expected_price = Decimal(10_000)
    real_price = select_result.price

    assert expected_product == real_product
    assert expected_title == real_title
    assert expected_description == real_description
    assert expected_price == real_price


async def test_When_CallDeleteProductWithNotFoundId_Should_ReturnNone():
    async with async_database.session() as db, db.begin():
        product_orm = await tested_class.delete(1, db)

    expected_product = None
    real_product = product_orm

    assert expected_product == real_product


async def test_When_CallDeleteProductWithFoundId_Should_ReturnDeletedModel(
        filling_products,
):
    async with async_database.session() as db, db.begin():
        product_orm = await tested_class.delete(1, db)
        product = ProductSchemaOut.from_orm(product_orm)

    expected_product = {
        'id': 1,
        'title': 'product',
        'description': 'product',
        'price': 1_000,
    }
    real_product = product.dict()

    assert expected_product == real_product
