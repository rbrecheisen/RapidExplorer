from PySide6.QtCore import QObject, Signal, Slot
from queue import Queue
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import threading

Base = declarative_base()

class YourTable(Base):
    __tablename__ = 'your_table'
    id = Column(Integer, primary_key=True)
    column1 = Column(String)
    column2 = Column(String)

class DatabaseThread(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.engine = create_engine('sqlite:///db.sqlite3', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def run(self):
        session = self.Session()
        while True:
            operation, args, result_queue = self.queue.get()
            if operation == 'stop':
                break
            elif operation == 'select':
                query = session.query(*args)
                result_queue.put(query.all())
            elif operation in ('add', 'update', 'delete'):
                session.add(*args) if operation == 'add' else session.delete(*args)
                session.commit()
                result_queue.put(None)
        session.close()

class YourApp(QObject):
    def __init__(self):
        super().__init__()
        self.db_queue = Queue()
        self.db_thread = DatabaseThread(self.db_queue)
        self.db_thread.start()

    @Slot()
    def do_some_query(self):
        result_queue = Queue()
        self.db_queue.put(('select', (YourTable,), result_queue))
        result = result_queue.get()
        print(result)

    @Slot()
    def do_some_add(self):
        new_entry = YourTable(column1='value1', column2='value2')
        self.db_queue.put(('add', (new_entry,), Queue()))

    def stop(self):
        self.db_queue.put(('stop', None, None))
        self.db_thread.join()

if __name__ == "__main__":
    app = YourApp()
    app.do_some_add()
    app.do_some_query()
    app.stop()
