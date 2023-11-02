from rapidx.app.data.db.db import Db
from rapidx.app.data.registrationhelper import RegistrationHelper
from rapidx.app.data.file.filemodelfactory import FileModelFactory
from rapidx.app.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory
from rapidx.app.data.db.dbinsertcommand import DbInsertCommand


class FileRegistrationHelper(RegistrationHelper):
    def __init__(self, path: str, db: Db) -> None:
        super(FileRegistrationHelper, self).__init__(name=None, path=path, db=db)
    
    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModelFactory.create()
        fileSetModel = FileSetModelFactory.create(multiFileSetModel=multiFileSetModel)
        fileModel = FileModelFactory.create(fileSetModel=fileSetModel, path=self.path())
        DbInsertCommand(self.db(), MultiFileSetModel, multiFileSetModel).execute()
        DbInsertCommand(self.db(), FileSetModel, fileSetModel).execute()
        DbInsertCommand(self.db(), FileModel, fileModel).execute()
        # self.db().add(multiFileSetModel)
        # self.db().add(fileSetModel)
        # self.db().add(fileModel)
        # self.db().commit()
        return multiFileSetModel
