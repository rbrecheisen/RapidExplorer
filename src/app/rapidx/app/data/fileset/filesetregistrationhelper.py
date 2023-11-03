from rapidx.app.data.db.db import Db
from rapidx.app.data.registrationhelper import RegistrationHelper
from rapidx.app.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory
from rapidx.app.data.db.dbaddcommand import DbAddCommand


class FileSetRegistrationHelper(RegistrationHelper):
    def __init__(self, name: str, path: str, db: Db) -> None:
        super(FileSetRegistrationHelper, self).__init__(name=name, path=path, db=db)

    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModelFactory().create()
        fileSetModel = FileSetModelFactory().create(name=self.name(), path=self.path(), multiFileSetModel=multiFileSetModel)
        DbAddCommand(self.db(), MultiFileSetModel, multiFileSetModel).execute()
        DbAddCommand(self.db(), FileSetModel, fileSetModel).execute()
        # self.db().add(multiFileSetModel)
        # self.db().add(fileSetModel)
        # self.db().commit()
        return multiFileSetModel
