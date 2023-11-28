from data.filetype import FileType
from data.registeredfilemodel import RegisteredFileModel


class JpegFileType(FileType):
    name = 'jpeg'

    def __init__(self) -> None:
        super(DicomFileType, self).__init__()

    def check(self, path: str) -> bool:
        if path.endswith('.jpg') or path.endswith('.jpeg'):
            return True
        return False
    
    def read(self, registeredFileModel: RegisteredFileModel):
        raise NotImplementedError('Not implemented yet')