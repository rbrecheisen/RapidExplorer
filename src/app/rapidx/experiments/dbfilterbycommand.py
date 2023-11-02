from dbresult import DbResult


class DbFilterByCommand:
    def __init__(self, db, model, id):
        self._db = db
        self._model = model
        self._kwargs = {'id': id}
        self._result = DbResult()

    def execute(self):
        self._db.queue().put((self._model, self._result, 'filterBy', None, self._kwargs))
        return self._result.get()