import asyncio
import platform
import sys
from asyncio import WindowsSelectorEventLoopPolicy

import pytest

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    if len(sys.argv) > 1:
        pytest.main(args=['--disable-warnings', '-vv', *sys.argv])
    else:
        pytest.main(args=['--disable-warnings', '-vv'])
