from data.filetype import FileType


class JpegFileType(FileType):
    @staticmethod
    def check(path: str) -> bool:
        if path.endswith('.jpg') or path.endswith('.jpeg'):
            return True
        return False
    
    @staticmethod
    def read(registeredFileModel: RegisteredFileModel):
        raise NotImplementedError('Not implemented yet')