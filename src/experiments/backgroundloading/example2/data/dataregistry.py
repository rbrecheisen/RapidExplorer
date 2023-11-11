import os

from data.engine import Engine
from data.databasesession import DatabaseSession
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.registeredfilemodel import RegisteredFileModel
from data.registeredfilesetmodel import RegisteredFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader
from data.filetype import FileType


class DataRegistry:
    def registerMultiFileSetModelForFile(self, path: str) -> RegisteredMultiFileSetModel:
        session = DatabaseSession(Engine().get()).get()
        try:
            multiFileSetModel = MultiFileSetModel()
            session.add(multiFileSetModel)
            fileSetModel = FileSetModel(multiFileSetModel=multiFileSetModel)
            session.add(fileSetModel)
            fileModel = FileModel(path=path, fileSetModel=fileSetModel)
            session.add(fileModel)
            session.commit()

            # Build registered data objects
            modelLoader = RegisteredMultiFileSetModelLoader()
            registeredMultiFileSetModel = modelLoader.load(multiFileSetModel.id)
            return registeredMultiFileSetModel
        finally:
            session.close()

    def registerMultiFileSetModelForFileSet(self, path: str, fileType: FileType) -> RegisteredMultiFileSetModel:
        session = DatabaseSession(Engine().get()).get()
        try:
            multiFileSetModel = MultiFileSetModel()
            session.add(multiFileSetModel)
            fileSetModel = FileSetModel(path=path, multiFileSetModel=multiFileSetModel)
            session.add(fileSetModel)
            fileModels = []
            for root, dirs, files in os.walk(path):
                for f in files:
                    fileName = f
                    filePath = os.path.join(root, fileName)
                    if fileType.check(filePath):
                        fileModel = FileModel(path=filePath, fileSetModel=fileSetModel)
                        fileModels.append(fileModel)
                        session.add(fileModel)                        
            session.commit()

            # Build registered data objects
            modelLoader = RegisteredMultiFileSetModelLoader()
            registeredMultiFileSetModel = modelLoader.load(multiFileSetModel.id)
            return registeredMultiFileSetModel
        finally:
            session.close()

    def registerMultiFileSetModelForMultiFileSet(self, path: str, fileType: FileType) -> RegisteredMultiFileSetModel:
        session = DatabaseSession(Engine().get()).get()
        try:
            multiFileSetModel = MultiFileSetModel(path=path)
            session.add(multiFileSetModel)
            data = {}
            for root, dirs, files in os.walk(path):
                for f in files:
                    fileName = f
                    filePath = os.path.join(root, fileName)
                    if fileType.check(filePath):
                        fileSetPath = root
                        if fileSetPath not in data.keys():
                            data[fileSetPath] = []
                        data[fileSetPath].append(filePath)
            for fileSetPath in data.keys():
                fileSetName = os.path.relpath(fileSetPath, path)
                fileSetModel = FileSetModel(name=fileSetName, path=fileSetPath, multiFileSetModel=multiFileSetModel)
                session.add(fileSetModel)
                for filePath in data[fileSetPath]:
                    fileModel = FileModel(path=filePath, fileSetModel=fileSetModel)
                    session.add(fileModel)
            session.commit()

            # Build registered data objects
            modelLoader = RegisteredMultiFileSetModelLoader()
            registeredMultiFileSetModel = modelLoader.load(multiFileSetModel.id)
            return registeredMultiFileSetModel
        finally:
            session.close()
