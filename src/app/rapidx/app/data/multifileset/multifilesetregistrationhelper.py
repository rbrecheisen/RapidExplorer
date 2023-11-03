from rapidx.app.data.db.db import Db
from rapidx.app.data.registrationhelper import RegistrationHelper
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory
from rapidx.app.data.db.dbaddcommand import DbAddCommand


class MultiFileSetRegistrationHelper(RegistrationHelper):
    def __init__(self, name: str, path: str, db: Db) -> None:
        super(MultiFileSetRegistrationHelper, self).__init__(name=name, path=path, db=db)
    
    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModelFactory().create(name=self.name(), path=self.path())
        DbAddCommand(self.db(), MultiFileSetModel, multiFileSetModel).execute()
        # self.db().add(multiFileSetModel)
        # self.db().commit()
        return multiFileSetModel
