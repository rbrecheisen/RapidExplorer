from rapidx.app.data.db.db import Db
from rapidx.app.data.registrationhelper import RegistrationHelper
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.db.dbaddcommand import DbAddCommand


class FileRegistrationHelper(RegistrationHelper):
    def __init__(self, path: str, db: Db) -> None:
        super(FileRegistrationHelper, self).__init__(name=None, path=path, db=db)
    
    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModel()
        multiFileSetModel = DbAddCommand(self.db(), MultiFileSetModel, multiFileSetModel).execute()
        fileSetModel = FileSetModel(multiFileSetModel)
        fileSetModel = DbAddCommand(self.db(), FileSetModel, fileSetModel).execute()
        fileModel = FileModel(fileSetModel, path=self.path())
        fileModel = DbAddCommand(self.db(), FileModel, fileModel).execute()
        return multiFileSetModel
