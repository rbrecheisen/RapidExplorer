from queue import Queue
from threading import Thread
from typing import List
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from rapidx.app.singleton import Singleton, singleton
from rapidx.app.data.basemodel import BaseModel

DATABASE = 'db.sqlite3'
ECHO = False


class Db(Singleton, Thread):
    def __init__(self, engine=None) -> None:
        super(Db, self).__init__()
        self._engine = engine
        if not self._engine:
            self._engine = create_engine(f'sqlite:///{DATABASE}', echo=ECHO)
            BaseModel.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        self._queue = Queue()
        self.daemon = True
        self.start()

    def engine(self):
        return self._engine

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
                    obj = self.session().get(model, obj.id)
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

    def close(self):
        self.session().close()

    # def __enter__(self):
    #     return self
    
    # def __exit__(self, exc_type, exc_value, traceback):
    #     self.session().close()