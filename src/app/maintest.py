import os
import pytest

DATABASE = 'db.test.sqlite3'


if __name__ == '__main__':
    if os.path.isfile(DATABASE):
        os.remove(DATABASE)
    pytest.main(['-s', 'src/app'])
    # pytest.main(['-m', 'not long_running', '-s', 'src/app'])
    # pytest.main(['-m', 'plugins', '-s', 'src/app'])