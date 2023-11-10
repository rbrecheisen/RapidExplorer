from rapidx.app.data.db.dbcommand import DbCommand


class DbCountChildrenCommand(DbCommand):
    def __init__(self, db, model, **kwargs):
        super(DbCountChildrenCommand, self).__init__(db, model, None, **kwargs)
        self.setCmd('countChildren')
