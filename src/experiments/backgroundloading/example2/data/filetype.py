from data.file import File
from data.registeredfilemodel import RegisteredFileModel


class FileType:
    def __init__(self, name: str) -> None:
        self.name = name
        self.loaded = False

    def check(self, path: str) -> bool:
        raise NotImplementedError('Not implemented')
    
    def read(self, registeredFileModel: RegisteredFileModel) -> File:
        raise NotImplementedError('Not implemented')