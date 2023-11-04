from rapidx.app.data.db.dbcommand import DbCommand


class DbGetCommand(DbCommand):
    def __init__(self, db, model, objId):
        super(DbGetCommand, self).__init__(db, model, objId)
        self.setCmd('get')
