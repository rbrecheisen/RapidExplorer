import os
import pytest


if __name__ == '__main__':
    os.remove('db.test.sqlite3')
    # pytest.main(['-s', 'src/app'])
    pytest.main(['-m', 'not long_running', '-s', 'src/app'])