from queue import Queue
from threading import Thread
from typing import List
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

# from rapidx.app.singleton import singleton
from rapidx.app.singleton import Singleton
from rapidx.app.data.basemodel import BaseModel
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel

DATABASE = 'db.sqlite3'
ECHO = False


class Db(Singleton, Thread):
    def __init__(self, engine=None) -> None:
        super(Db, self).__init__()
        if not engine:
            engine = create_engine(f'sqlite:///{DATABASE}', echo=ECHO)
            Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self._session = Session()
        self._queue = Queue()
        self.daemon = True
        self.start()

    def session(self) -> Session:
        return self._session
    
    def queue(self) -> Queue:
        return self._queue

    def run(self) -> None:
        while True:
            queueInput = self.queue().get()
            model, result, operation, obj, kwargs = queueInput
            try:
                if operation == 'add':
                    self.session().add(obj)
                    self.session().commit()
                    result.set(obj)
                elif operation == 'update':
                    objId = obj
                    obj = self.session().get(model, objId)
                    for k, v in kwargs.items():
                        setattr(obj, k, v)
                    self.session().commit()
                    result.set(obj)
                elif operation == 'delete':
                    objId = obj
                    obj = self.session().get(model, objId)
                    self.session().delete(obj)
                    self.session().commit()
                    result.set(True)
                elif operation == 'filterBy':
                    objs = self.session().query(model).filter_by(**kwargs).all()
                    result.set(objs)
                elif operation == 'get':
                    objId = obj
                    obj = self.session().get(model, objId)
                    result.set(obj)
                elif operation == 'queryAll':
                    objs = self.session().query(model).all()
                    result.set(objs)
                elif operation == 'stop':
                    break
                else:
                    result.set(False)
            except Exception as e:
                result.setException(e)
            finally:
                self.queue().task_done()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.session().close()

# # TODO: Use a base class instead of a decorator!
# @singleton
# class Db(Thread):
#     def __init__(self, queue, engine=None):
#         super(Db, self).__init__()
#         self._queue = queue
#         if not engine:
#             engine = create_engine(f'sqlite:///{DATABASE}', echo=ECHO)
#             BaseModel.metadata.create_all(engine)
#         self._session = Session(engine)

#     def queue(self) -> Queue:
#         return self._queue

#     def add(self, obj):
#         self._session.add(obj)

#     def commit(self):
#         self._session.commit()

#     def close(self):
#         self._session.close()

#     def loadAll(self) -> List[MultiFileSetModel]:
#         return self._session.query(MultiFileSetModel).all()
    
#     def loadMultiFileSetModel(self, multiFileSetModelId: str) -> MultiFileSetModel:
#         return self._session.get(MultiFileSetModel, multiFileSetModelId)
    
#     def loadFileSetModels(self, multiFileSetModelId: str) -> List[FileSetModel]:
#         return self._session.query(FileSetModel).filter_by(_multiFileSetModelId=multiFileSetModelId)
    
#     def loadFileModels(self, fileSetModelId: str) -> List[FileModel]:
#         return self._session.query(FileModel).filter_by(_fileSetModelId=fileSetModelId).all()

#     def __enter__(self):
#         return self
    
#     def __exit__(self, exc_type, exc_value, traceback):
#         self._session.close()