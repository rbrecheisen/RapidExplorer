import pytest


if __name__ == '__main__':
    pytest.main(['-m', 'not long_running', '-s', 'src/app'])