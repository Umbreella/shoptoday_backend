from fastapi import FastAPI

from routers import (billing_account_router, buy_router, product_router,
                     token_router, transaction_router, user_router,
                     webhook_router)


def add_routers(app: FastAPI):
    app.include_router(**{
        'router': user_router.router,
        'prefix': '/api/users',
    })
    app.include_router(**{
        'router': product_router.router,
        'prefix': '/api/products',
    })
    app.include_router(**{
        'router': billing_account_router.router,
        'prefix': '/api/billing_accounts',
    })
    app.include_router(**{
        'router': transaction_router.router,
        'prefix': '/api/transactions',
    })
    app.include_router(**{
        'router': buy_router.router,
        'prefix': '/api/buy',
    })
    app.include_router(**{
        'router': token_router.router,
        'prefix': '/api',
    })
    app.include_router(**{
        'router': webhook_router.router,
        'prefix': '',
    })

    return app
