from data.filetype import FileType
from data.registeredfilemodel import RegisteredFileModel


class PngFileType(FileType):
    def __init__(self) -> None:
        super(DicomFileType, self).__init__(name='png')

    def check(self, path: str) -> bool:
        if path.endswith('.png'):
            return True
        return False
    
    def read(self, registeredFileModel: RegisteredFileModel):
        raise NotImplementedError('Not implemented yet')