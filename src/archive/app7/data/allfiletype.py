from data.filetype import FileType


class AllFileType(FileType):
    NAME = 'all'
    
    @staticmethod
    def check(filePath: str) -> bool:
        return True