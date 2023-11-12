from typing import List

from data.dbsession import DbSession
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.registeredfilemodel import RegisteredFileModel
from data.registeredfilesetmodel import RegisteredFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class RegisteredMultiFileSetModelLoader:
    def loadAll(self) -> List[RegisteredMultiFileSetModel]:
        registeredMultiFileSetModels = []
        with DbSession() as session:
            multiFileSetModels = session.query(MultiFileSetModel).all()
            for multiFileSetModel in multiFileSetModels:
                registeredMultiFileSetModels.append(self.load(multiFileSetModel.id))
            return registeredMultiFileSetModels

    def load(self, registeredMultiFileSetModelId: str) -> RegisteredMultiFileSetModel:
        with DbSession() as session:
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