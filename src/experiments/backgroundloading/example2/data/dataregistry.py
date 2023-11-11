from data.engine import Engine
from data.databasesession import DatabaseSession
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.registeredfilemodel import RegisteredFileModel
from data.registeredfilesetmodel import RegisteredFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class DataRegistry:
    def registerMultiFileSetModelFromFilePath(self, path: str) -> RegisteredMultiFileSetModel:
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
            registeredMultiFileSetModel = RegisteredMultiFileSetModel(multiFileSetModel=multiFileSetModel)
            registeredFileSetModel = RegisteredFileSetModel(fileSetModel=fileSetModel, registeredMultiFileSetModel=registeredMultiFileSetModel)
            registeredFileModel = RegisteredFileModel(fileModel=fileModel, registeredFileSetModel=registeredFileSetModel)
            # Setup relations
            registeredMultiFileSetModel.registeredFileSetModels.append(registeredFileSetModel)
            registeredFileSetModel.registeredFileModels.append(registeredFileModel)
            return registeredMultiFileSetModel
        finally:
            session.close()
