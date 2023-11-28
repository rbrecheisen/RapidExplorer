import os

from data.registrar import Registrar
from data.dbsession import DbSession
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader
from data.filetype import FileType


class FileRegistrar(Registrar):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(FileRegistrar, self).__init__(path=path, fileType=fileType)

    def execute(self) -> RegisteredMultiFileSetModel:        
        with DbSession() as session:
            multiFileSetModel = MultiFileSetModel()
            session.add(multiFileSetModel)
            fileSetModel = FileSetModel(multiFileSetModel=multiFileSetModel)
            session.add(fileSetModel)
            if self.fileType().check(self.path()):
                fileName = os.path.split(self.path())[1]
                fileModel = FileModel(path=self.path(), name=fileName, fileSetModel=fileSetModel, fileType=self.fileType().name)
                session.add(fileModel)
                session.commit()

            # Build registered data objects
            modelLoader = RegisteredMultiFileSetModelLoader()
            registeredMultiFileSetModel = modelLoader.load(multiFileSetModel.id)
            return registeredMultiFileSetModel