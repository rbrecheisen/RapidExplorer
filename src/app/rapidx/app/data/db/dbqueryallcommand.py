from rapidx.app.data.db.dbcommand import DbCommand


class DbQueryAllCommand(DbCommand):
    def __init__(self, db, model, obj=None, **kwargs):
        super(DbQueryAllCommand, self).__init__(db, model, obj, **kwargs)
        self.setCmd('queryAll')
