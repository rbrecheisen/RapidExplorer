from data.file import File
from data.registeredfilemodel import RegisteredFileModel


class FileType:
    name = None
    def __init__(self) -> None:
        self.loaded = False

    def check(self, path: str) -> bool:
        raise NotImplementedError('Not implemented')
    
    def read(self, registeredFileModel: RegisteredFileModel) -> File:
        raise NotImplementedError('Not implemented')