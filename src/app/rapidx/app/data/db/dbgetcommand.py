from rapidx.app.data.db.dbcommand import DbCommand


class DbGetCommand(DbCommand):
    def __init__(self, db, model, obj, **kwargs):
        super(DbGetCommand, self).__init__(db, model, obj, **kwargs)
        self.setCmd('get')
