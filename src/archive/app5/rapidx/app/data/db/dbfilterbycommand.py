from rapidx.app.data.db.dbcommand import DbCommand


class DbFilterByCommand(DbCommand):
    def __init__(self, db, model, **kwargs):
        super(DbFilterByCommand, self).__init__(db, model, None, **kwargs)
        self.setCmd('filterBy')
