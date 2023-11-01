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


class Db(Singleton, Thread):
    """ The Db class is a singleton. It holds a single database connection to SQLite3.
    In order to do something with the database, you need to call some methods, e.g.,
    loadAll(), loadMultiFileSetModel(multiFileSetModelId=?) or whatever. 

    The problem is you cannot directly call methods on this class. You have to use
    the queue mechanism. So you need to find a way to convert the potentially complicated
    session calls to something you can add to the queue. 

    For example, instead of having this:

        def loadFileSetModel(self, id):
            return session.query(FileSetModel).filter_by(_multiFileSetModelId=id)

    could be translated to:

        with Db() as db:
            result = Future()  # Make class DbResult(Future)?
            db.queue().put((FileSetModel, result, 'filter_by', multiFileSetModelId=id))
            # Alternatively: db.loadFileSetModel() that internally puts stuff to the queue? Can I access this method if Db is a running thread?
            print(result)

    where the Db class run() method would process it as follows:

        model, operation, result, kwargs = self.queue().get()
        try:
            if operation == 'filter_by':
                result.set_result(self.session().query(model).filter_by(**kwargs)).all()  # Becomes result.set() if you have DbResult class
            elif operation == 'query':
                result.set_result(self.session().query(model).all())  # Perhaps make operation "all" or "queryAll", and "queryOne", etc.
            else:
                pass
        except Exception as e:  # What exceptions can Session throw?
            result.set_exception(e)

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
            result = Future()
            db.queue().put((YourTable, result, 'filterBy', None, {'id': id}))
            for obj in result.result():
                print(obj)

    def doQueryAll(self):
        with Db() as db:
            result = Future()
            db.queue().put((YourTable, 'queryAll', result))
            print(result.result())

    def stop(self):
        with Db() as db:
            db.queue().put((None, None, 'stop', None, None))
            db.join()

if __name__ == "__main__":
    app = YourApp()
    app.doFilterBy(id=1)
    app.stop()
