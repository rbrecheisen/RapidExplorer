import pendulum
import importlib

from data import engine
from data.dbsession import DbSession
# from data.multifilesetmodel import MultiFileSetModel


def createRandomName(prefix: str=''):
    tz = pendulum.local_timezone()
    timestamp = pendulum.now(tz).strftime('%Y%m%d%H%M%S')
    if prefix != '' and not prefix.endswith('-'):
        prefix = prefix + '-'
    name = f'{prefix}{timestamp}'
    return name


def clearDatabase():
    print(f'Clearing database: {engine.DATABASE}')
    with DbSession() as session:
        # Get MultiFileSetModel class without having to directly import it because
        # this will result in circular import problems
        modelClass = getattr(importlib.import_module('data.multifilesetmodel'), 'MultiFileSetModel')
        multiFileSetModels = session.query(modelClass).all()
        for multiFileSetModel in multiFileSetModels:
            session.delete(multiFileSetModel)
