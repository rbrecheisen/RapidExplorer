from rapidx.app.data.db import Db
from rapidx.app.data.registrationhelper import RegistrationHelper
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory


class MultiFileSetRegistrationHelper(RegistrationHelper):
    def __init__(self, name: str, path: str, db: Db) -> None:
        super(MultiFileSetRegistrationHelper, self).__init__(name=name, path=path, db=db)
    
    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModelFactory.create(name=self.name(), path=self.path())
        self.db().add(multiFileSetModel)
        self.db().commit()
        return multiFileSetModel
