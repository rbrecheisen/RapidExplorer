import os
import pytest

from data import engine

engine.DATABASE = 'db.test.sqlite3'
engine.ECHO = False


if __name__ == '__main__':
    if os.path.isfile(engine.DATABASE):
        os.remove(engine.DATABASE)
    # pytest.main(['-s', 'src/app'])
    pytest.main(['-m', 'plugin', '-s', 'src/app'])
    # pytest.main(['-m', 'not long_running', '-s', 'src/app'])