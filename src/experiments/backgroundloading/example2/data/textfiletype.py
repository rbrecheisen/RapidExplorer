from data.filetype import FileType


class TextFileType(FileType):
    def __init__(self) -> None:
        super(TextFileType, self).__init__(name='text')

    def check(self, path: str) -> bool:
        if path.endswith('.txt'):
            return True
        return False
    
    def read(self, registeredFileModel: RegisteredFileModel):
        raise NotImplementedError('Not implemented yet')