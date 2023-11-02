from rapidx.app.data.db.dbresult import DbResult


class DbCommand:
    def __init__(self, db, model, obj, **kwargs):
        self._db = db
        self._model = model
        self._obj = obj
        self._kwargs = kwargs
        self._result = DbResult()
        self._cmd = 'unknown'

    def setCmd(self, cmd: str):
        self._cmd = cmd

    def execute(self):
        self._db.queue().put((self._model, self._result, self._cmd, self._obj, self._kwargs))
        return self._result.get()