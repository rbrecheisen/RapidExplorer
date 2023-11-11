from data.filetype import FileType
from data.registeredfilemodel import RegisteredFileModel


class PngFileType(FileType):
    @staticmethod
    def check(path: str) -> bool:
        if path.endswith('.png'):
            return True
        return False
    
    @staticmethod
    def read(registeredFileModel: RegisteredFileModel):
        raise NotImplementedError('Not implemented yet')