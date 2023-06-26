import sys

import pytest

if __name__ == '__main__':
    if len(sys.argv) > 1:
        pytest.main(args=['--disable-warnings', '-vv', *sys.argv])
    else:
        pytest.main(args=['--disable-warnings', '-vv'])
