from rapidx.app.data.db.dbcommand import DbCommand


class DbQueryAllCommand(DbCommand):
    def __init__(self, db, model, obj, **kwargs):
        super(DbInsertCommand, self).__init__(db, model, obj, kwargs)
        self.setCmd('queryAll')
