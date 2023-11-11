import os
import pytest

DATABASE = 'db.experiments.sqlite3'


if __name__ == '__main__':
    if os.path.isfile(DATABASE):
        os.remove(DATABASE)
    pytest.main(['-s', 'src/experiments/backgroundloading/example2'])