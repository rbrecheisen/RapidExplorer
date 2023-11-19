from rapidx.app.data.db.dbcommand import DbCommand


class DbAddCommand(DbCommand):
    def __init__(self, db, model, obj):
        super(DbAddCommand, self).__init__(db, model, obj)
        self.setCmd('add')
