import asyncio
import platform
from asyncio import WindowsSelectorEventLoopPolicy

import pytest

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    pytest.main(args=['--disable-warnings', '-vv', ])
