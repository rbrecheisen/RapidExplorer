from data.registeredfilemodel import RegisteredFileModel


class File:
    def __init__(self, registeredFileModel: RegisteredFileModel) -> None:
        self._registeredFileModel = registeredFileModel
        self.id = self._registeredFileModel.id   # Not using "_" to conform to SQL and registered models
        self.name = self._registeredFileModel.name

    def registeredFileModel(self) -> RegisteredFileModel:
        return self._registeredFileModel
    
    def data(self):
        raise NotImplementedError('Not implemented')