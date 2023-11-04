from rapidx.app.data.db.dbcommand import DbCommand


class DbDeleteCommand(DbCommand):
    def __init__(self, db, model, objId: int):
        super(DbDeleteCommand, self).__init__(db, model, objId)
        self.setCmd('delete')
