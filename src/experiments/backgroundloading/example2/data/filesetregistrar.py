import os

from utils import create_random_name
from data.registrar import Registrar
from data.dbsession import DbSession
# from data.dataregistry import DataRegistry
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader
from data.filetype import FileType


class FileSetRegistrar(Registrar):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(FileSetRegistrar, self).__init__()
        self._path = path
        self._fileType = fileType

    def execute(self) -> RegisteredMultiFileSetModel:
        with DbSession() as session:
            multiFileSetModel = MultiFileSetModel()
            session.add(multiFileSetModel)
            fileSetModel = FileSetModel(path=self._path, multiFileSetModel=multiFileSetModel)
            session.add(fileSetModel)
            fileModels = []
            for root, dirs, files in os.walk(self._path):
                for f in files:
                    fileName = f
                    filePath = os.path.join(root, fileName)
                    if self._fileType.check(filePath):
                        fileModel = FileModel(path=filePath, fileSetModel=fileSetModel)
                        fileModels.append(fileModel)
                        session.add(fileModel)                        
            session.commit()

            # Build registered data objects
            modelLoader = RegisteredMultiFileSetModelLoader()
            registeredMultiFileSetModel = modelLoader.load(multiFileSetModel.id)
            return registeredMultiFileSetModel

    # def execute(self) -> MultiFileSetModel:
    #     registry = DataRegistry()
    #     registeredMultiFileSetModel = registry.registerMultiFileSetModelForFileSet(self._path, self._fileType)
    #     return registeredMultiFileSetModel
