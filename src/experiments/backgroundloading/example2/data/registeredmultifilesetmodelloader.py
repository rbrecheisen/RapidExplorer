from typing import List

from data.engine import Engine
from data.databasesession import DatabaseSession
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.registeredfilemodel import RegisteredFileModel
from data.registeredfilesetmodel import RegisteredFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class RegisteredMultiFileSetModelLoader:
    def loadAll(self) -> List[RegisteredMultiFileSetModel]:
        registeredMultiFileSetModels = []
        session = DatabaseSession(Engine().get()).get()
        try:
            multiFileSetModels = session.query(MultiFileSetModel).all()
            for multiFileSetModel in multiFileSetModels:
                # Looks like load() can create its own session without issues (same engine anyway)
                registeredMultiFileSetModels.append(self.load(multiFileSetModel.id))
            return registeredMultiFileSetModels
        finally:
            session.close()

    def load(self, registeredMultiFileSetModelId: str) -> RegisteredMultiFileSetModel:
        session = DatabaseSession(Engine().get()).get()
        try:
            multiFileSetModel = session.get(MultiFileSetModel, registeredMultiFileSetModelId)
            registeredMultiFileSetModel = RegisteredMultiFileSetModel(multiFileSetModel=multiFileSetModel)
            fileSetModels = session.query(FileSetModel).filter_by(multiFileSetModel=multiFileSetModel).all()
            for fileSetModel in fileSetModels:
                registeredFileSetModel = RegisteredFileSetModel(fileSetModel=fileSetModel, registeredMultiFileSetModel=registeredMultiFileSetModel)
                registeredMultiFileSetModel.registeredFileSetModels.append(registeredFileSetModel)
                fileModels = session.query(FileModel).filter_by(fileSetModel=fileSetModel).all()
                for fileModel in fileModels:
                    registeredFileModel = RegisteredFileModel(fileModel=fileModel, registeredFileSetModel=registeredFileSetModel)
                    registeredFileSetModel.registeredFileModels.append(registeredFileModel)
            return registeredMultiFileSetModel
        finally:
            session.close()