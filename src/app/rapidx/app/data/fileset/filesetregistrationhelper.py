import os

from rapidx.app.data.db.db import Db
from rapidx.app.data.registrationhelper import RegistrationHelper
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.db.dbaddcommand import DbAddCommand


class FileSetRegistrationHelper(RegistrationHelper):
    def __init__(self, name: str, path: str, db: Db) -> None:
        super(FileSetRegistrationHelper, self).__init__(name=name, path=path, db=db)

    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModel()
        multiFileSetModel = DbAddCommand(self.db(), MultiFileSetModel, multiFileSetModel).execute()
        fileSetModel = FileSetModel(multiFileSetModel, name=self.name(), path=self.path())
        fileSetModel = DbAddCommand(self.db(), FileSetModel, fileSetModel).execute()
        files = os.listdir(fileSetModel.path)
        for f in files:
            fileName = f
            filePath = os.path.join(fileSetModel.path, fileName)
            fileModel = FileModel(fileSetModel, path=filePath)
            DbAddCommand(self.db(), FileModel, fileModel).execute()
        return multiFileSetModel
