from typing import Any
from queue import Queue
from threading import Thread
from PySide6.QtCore import QObject, Slot
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from concurrent.futures import Future

DATABASE = 'db.sqlite3'
ECHO = False

Base = declarative_base()


class YourTable(Base):
    __tablename__ = 'your_table'
    id = Column(Integer, primary_key=True)
    column1 = Column(String)
    column2 = Column(String)

    def __str__(self):
        return f'YourTable(colum1={self.column1}, column2={self.column2})'


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
    

class DbResult(Future):
    def __init__(self) -> None:
        super(DbResult, self).__init__()

    def get(self) -> Any:
        return self.result()

    def set(self, obj: Any):
        self.set_result(obj)

    def setException(self, obj: Any):
        self.set_exception(obj)


class Db(Singleton, Thread):
    """
    Needed classes:
    ---------------
    DbResult(Future):           Class that holds future containing results of database operation
    DbCommand:                  Base class for database commands
    DbInsertCommand(DbCommand): Class for insert object into the database
    DbUpdateCommand(DbCommand): Class for updating existing objects in the database
    DbDeleteCommand(DbCommand): Class for deleting objects from the database

    TODO: Add methods below to Db class itself doesn't work. They need to be defined
    outside of the thread and used by the client. Work with Command classes, e.g.,
        - LoadAllCommand()
        - LoadMultiFileSetModelCommand(multiFileSetModelId)
        - LoadFileSetModelsCommand(multiFileSetModelId)
        - LoadFileModels(fileSetModelId)

    Classes affected:
        - FileRegistrationHelper
        - ModelFactory
        - ModelImporter
    """
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
            if len(queueInput) == 5:
                model, result, operation, args, kwargs = queueInput
                try:
                    if operation == 'filterBy':
                        x = self.session().query(model).filter_by(**kwargs).all()
                        result.set_result(x)
                    elif operation == 'queryAll':
                        result.set_result(self.session().query(model).all())
                    elif operation == 'stop':
                        break
                    else:
                        result.set_result(False)
                except Exception as e:
                    result.set_exception(e)
                finally:
                    self.session().commit()
                    self.queue().task_done()
            else:
                print(f'len(queueInput): {len(queueInput)}, queueInput: {queueInput}')

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.session().close()


class YourApp(QObject):
    def __init__(self):
        super().__init__()

    def doFilterBy(self, id: int):
        with Db() as db:
            # db.loadMultiFileSetModel(multiFileSetModelId=id)  DOESN'T WORK!
            result = Future()
            db.queue().put((YourTable, result, 'filterBy', None, {'id': id}))
            for obj in result.result():
                print(obj)

    def doQueryAll(self):
        with Db() as db:
            result = Future()
            db.queue().put((YourTable, result, 'queryAll', None, None))
            print(result.result())

    def stop(self):
        with Db() as db:
            db.queue().put((None, None, 'stop', None, None))
            db.join()

if __name__ == "__main__":
    app = YourApp()
    app.doFilterBy(id=1)
    app.doQueryAll()
    app.stop()
