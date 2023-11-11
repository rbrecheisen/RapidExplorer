from data.file import File
from data.registeredfilemodel import RegisteredFileModel


class FileType:
    @staticmethod
    def check(path: str) -> bool:
        raise NotImplementedError('Not implemented')
    
    @staticmethod
    def read(registeredFileModel: RegisteredFileModel) -> File:
        raise NotImplementedError('Not implemented')