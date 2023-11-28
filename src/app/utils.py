import pendulum
import importlib

from data import engine
from data.dbsession import DbSession


def createRandomName(prefix: str=''):
    tz = pendulum.local_timezone()
    timestamp = pendulum.now(tz).strftime('%Y%m%d%H%M%S%f')[:17]
    if prefix != '' and not prefix.endswith('-'):
        prefix = prefix + '-'
    name = f'{prefix}{timestamp}'
    return name


def clearDatabase():
    print(f'Clearing database: {engine.DATABASE}')
    with DbSession() as session:
        pass