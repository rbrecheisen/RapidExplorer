from queue import Queue
from threading import Thread
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from rapidx.app.singleton import singleton
from rapidx.app.data.basemodel import BaseModel
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel

DATABASE = 'db.sqlite3'
ECHO = False


# TODO: Use a base class instead of a decorator!
@singleton
class Db(Thread):
    def __init__(self, queue, engine=None):
        super(Db, self).__init__()
        self._queue = queue
        if not engine:
            engine = create_engine(f'sqlite:///{DATABASE}', echo=ECHO)
            BaseModel.metadata.create_all(engine)
        self._session = Session(engine)

    def queue(self) -> Queue:
        return self._queue

    def add(self, obj):
        self._session.add(obj)

    def commit(self):
        self._session.commit()

    def close(self):
        self._session.close()

    def loadAll(self) -> List[MultiFileSetModel]:
        return self._session.query(MultiFileSetModel).all()
    
    def loadMultiFileSetModel(self, multiFileSetModelId: str) -> MultiFileSetModel:
        return self._session.get(MultiFileSetModel, multiFileSetModelId)
    
    def loadFileSetModels(self, multiFileSetModelId: str) -> List[FileSetModel]:
        return self._session.query(FileSetModel).filter_by(_multiFileSetModelId=multiFileSetModelId)
    
    def loadFileModels(self, fileSetModelId: str) -> List[FileModel]:
        return self._session.query(FileModel).filter_by(_fileSetModelId=fileSetModelId).all()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()