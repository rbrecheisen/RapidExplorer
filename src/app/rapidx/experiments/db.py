from queue import Queue
from threading import Thread
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker

from singleton import Singleton
from dbresult import DbResult
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
        return f'YourTable(colum1={self.column1}, column2={self.column2})'


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


if __name__ == '__main__':
    def testDb():
        with Db() as db:
            command = DbFilterByCommand(db, YourTable, 1)
            results = command.execute()
            for result in results:
                print(result)
    testDb()