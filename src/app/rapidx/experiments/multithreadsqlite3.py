import sqlite3
import threading

from queue import Queue
from PySide6.QtCore import QObject, Signal, Slot


class DbThread(threading.Thread):
    def __init__(self, queue) -> None:
        super(DbThread, self).__init__()
        self._queue = queue

    def queue(self) -> Queue:
        return self._queue
    
    def run(self) -> None:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        while True:
            operation, args, resultQueue = self.queue().get()
            if operation == 'stop':
                break
            if operation == 'select':
                cursor.execute(*args)
                resultQueue.put(cursor.fetchAll())
                continue
            if operation in ('insert', 'update', 'delete'):
                cursor.execute(*args)
                conn.commit()
                resultQueue.put(None)
                continue
        conn.close()


class YourApp(QObject):
    def __init__(self) -> None:
        super(YourApp, self).__init__()
        self._dbQueue = Queue()
        self._dbThread = DbThread(self._dbQueue)
        self._dbThread.start()

    @Slot()
    def  doSomeInsert(self):
        self._dbQueue.put((
            'insert', 
            ('INSERT INTO your_table (column1, column2) VALUES (?, ?)', ('value1', 'value2')), 
            Queue()
        ))

    def stop(self):
        self._dbQueue.put(('stop', None, None))
        self._dbThread.join()


if __name__ == '__main__':
    app = YourApp()
    app.doSomeInsert()
    app.stop()
