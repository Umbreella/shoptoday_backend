import asyncio
import platform
from asyncio import WindowsSelectorEventLoopPolicy

import uvicorn

from app.app import get_asgi_application

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    uvicorn.run(get_asgi_application())
