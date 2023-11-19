from data.filesetmodel import FileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class RegisteredFileSetModel:
    def __init__(self, fileSetModel: FileSetModel, registeredMultiFileSetModel: RegisteredMultiFileSetModel) -> None:
        self.id = fileSetModel.id
        self.name = fileSetModel.name
        self.path = fileSetModel.path
        self.registeredMultiFileSetModel = registeredMultiFileSetModel
        self.registeredFileModels = []
        self.loaded = False

    def nrFiles(self) -> int:
        return len(self.registeredFileModels)