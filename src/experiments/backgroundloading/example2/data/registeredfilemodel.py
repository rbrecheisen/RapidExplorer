from data.filemodel import FileModel
from data.registeredfilesetmodel import RegisteredFileSetModel


class RegisteredFileModel:
    def __init__(self, fileModel: FileModel, registeredFileSetModel: RegisteredFileSetModel) -> None:
        self.id = fileModel.id
        self.name = None
        self.path = fileModel.path
        self.fileType = fileModel.fileType
        self.registeredFileSetModel = registeredFileSetModel
        self.loaded = False
