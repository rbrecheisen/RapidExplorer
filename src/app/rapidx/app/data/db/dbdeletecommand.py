from rapidx.app.data.db.dbcommand import DbCommand


class DbDeleteCommand(DbCommand):
    def __init__(self, db, model, obj, **kwargs):
        super(DbDeleteCommand, self).__init__(db, model, obj, kwargs)
        self.setCmd('delete')
