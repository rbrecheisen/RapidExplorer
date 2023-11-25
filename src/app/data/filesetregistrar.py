import os

from data.registrar import Registrar
from data.dbsession import DbSession
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader
from data.filetype import FileType


class FileSetRegistrar(Registrar):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(FileSetRegistrar, self).__init__(path=path, fileType=fileType)

    def execute(self) -> RegisteredMultiFileSetModel:
        with DbSession() as session:
            multiFileSetModel = MultiFileSetModel()
            session.add(multiFileSetModel)
            fileSetModel = FileSetModel(path=self.path(), multiFileSetModel=multiFileSetModel)
            session.add(fileSetModel)
            fileModels = []
            for root, dirs, files in os.walk(self.path()):
                for f in files:
                    fileName = f
                    filePath = os.path.join(root, fileName)
                    if self.fileType().check(filePath):
                        fileName = os.path.split(filePath)[1]
                        fileModel = FileModel(path=filePath, name=fileName, fileSetModel=fileSetModel, fileType=self.fileType().name)
                        fileModels.append(fileModel)
                        session.add(fileModel)      
            session.commit()

            # Build registered data objects
            modelLoader = RegisteredMultiFileSetModelLoader()
            registeredMultiFileSetModel = modelLoader.load(multiFileSetModel.id)
            return registeredMultiFileSetModel