from rapidx.app.data.db.dbcommand import DbCommand


class DbUpdateCommand(DbCommand):
    def __init__(self, db, model, obj, **kwargs):
        super(DbUpdateCommand, self).__init__(db, model, obj, **kwargs)
        self.setCmd('update')
