from queue import Queue
from threading import Thread
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker

from singleton import Singleton
from dbinsertcommand import DbInsertCommand
from dbdeletecommand import DbDeleteCommand
from dbgetcommand import DbGetCommand
from dbupdatecommand import DbUpdateCommand
from dbfilterbycommand import DbFilterByCommand

DATABASE = 'db.sqlite3'
ECHO = False

Base = declarative_base()


class YourTable(Base):
    __tablename__ = 'your_table'
    id = Column(Integer, primary_key=True)
    column1 = Column(String)
    column2 = Column(String)

    def __str__(self):
        return f'YourTable(id={self.id}, colum1={self.column1}, column2={self.column2})'


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
            model, result, operation, args, kwargs = queueInput
            try:
                if operation == 'insert':
                    obj = model(**kwargs)
                    self.session().add(obj)
                    self.session().commit()
                    result.set(obj)
                elif operation == 'update':
                    obj = self.session().get(model, *args)
                    for k, v in kwargs.items():
                        setattr(obj, k, v)
                    self.session().commit()
                    result.set(obj)
                elif operation == 'delete':
                    obj = self.session().get(model, *args)
                    self.session().delete(obj)
                    self.session().commit()
                    result.set(True)
                elif operation == 'filterBy':
                    objs = self.session().query(model).filter_by(**kwargs).all()
                    result.set(objs)
                elif operation == 'get':
                    obj = self.session().get(model, *args)
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


if __name__ == '__main__':
    def testDb():
        with Db() as db:
            command = DbInsertCommand(db, YourTable, column1='value1', column2='value2')
            obj = command.execute()
            command = DbGetCommand(db, YourTable, obj.id)
            obj = command.execute()
            assert obj.column1 == 'value1'
            command = DbUpdateCommand(db, YourTable, obj.id, column1='value3')
            obj = command.execute()
            assert obj.column1 == 'value3'
            command = DbDeleteCommand(db, YourTable, obj.id)
            command.execute()
            command = DbGetCommand(db, YourTable, obj.id)
            results = command.execute()
            assert not results
    testDb()