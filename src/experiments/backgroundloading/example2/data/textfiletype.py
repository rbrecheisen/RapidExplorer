from data.filetype import FileType


class TextFileType(FileType):
    @staticmethod
    def check(path: str) -> bool:
        if path.endswith('.txt'):
            return True
        return False
    
    @staticmethod
    def read(registeredFileModel: RegisteredFileModel):
        raise NotImplementedError('Not implemented yet')