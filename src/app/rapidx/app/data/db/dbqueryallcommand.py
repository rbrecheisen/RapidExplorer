from rapidx.app.data.db.dbcommand import DbCommand


class DbQueryAllCommand(DbCommand):
    def __init__(self, db, model):
        super(DbQueryAllCommand, self).__init__(db, model, None)
        self.setCmd('queryAll')
