import os
import pytest

from mosamaticdesktop.data import engine

engine.DATABASE = 'db.test.sqlite3'
engine.ECHO = False


if __name__ == '__main__':
    if os.path.isfile(engine.DATABASE):
        os.remove(engine.DATABASE)
    # if os.path.isfile('mosamaticdesktop/aiservice/db.sqlite3'):
    #     os.remove('mosamaticdesktop/aiservice/db.sqlite3')
    pytest.main(['-s', 'mosamaticdesktop/test'])