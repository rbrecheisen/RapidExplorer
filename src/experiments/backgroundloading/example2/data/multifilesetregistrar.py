import os

from data.registrar import Registrar
from data.dbsession import DbSession
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader
from data.filetype import FileType


class MultiFileSetRegistrar(Registrar):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(MultiFileSetRegistrar, self).__init__(path=path, fileType=fileType)

    def execute(self) -> RegisteredMultiFileSetModel:
        with DbSession() as session:
            multiFileSetModel = MultiFileSetModel(path=self.path())
            session.add(multiFileSetModel)
            data = {}
            for root, dirs, files in os.walk(self.path()):
                for f in files:
                    fileName = f
                    filePath = os.path.join(root, fileName)
                    if self.fileType().check(filePath):
                        fileSetPath = root
                        if fileSetPath not in data.keys():
                            data[fileSetPath] = []
                        data[fileSetPath].append(filePath)
            for fileSetPath in data.keys():
                fileSetName = os.path.relpath(fileSetPath, self.path())
                fileSetModel = FileSetModel(name=fileSetName, path=fileSetPath, multiFileSetModel=multiFileSetModel)
                session.add(fileSetModel)
                for filePath in data[fileSetPath]:
                    fileModel = FileModel(path=filePath, fileSetModel=fileSetModel, fileType=self.fileType().name)
                    session.add(fileModel)
            session.commit()

            # Build registered data objects
            modelLoader = RegisteredMultiFileSetModelLoader()
            registeredMultiFileSetModel = modelLoader.load(multiFileSetModel.id)
            return registeredMultiFileSetModel