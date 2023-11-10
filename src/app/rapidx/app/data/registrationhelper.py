from rapidx.app.data.db.db import Db


class RegistrationHelper:
    def __init__(self, name: str, path: str, db: Db) -> None:
        self._name = name
        self._path = path
        self._db = db

    def name(self) -> str:
        return self._name

    def path(self) -> str:
        return self._path

    def db(self) -> Db:
        return self._db