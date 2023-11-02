from rapidx.app.data.db.dbcommand import DbCommand


class DbFilterByCommand(DbCommand):
    def __init__(self, db, model, obj, **kwargs):
        super(DbFilterByCommand, self).__init__(db, model, obj, kwargs)
        self.setCmd('filterBy')
