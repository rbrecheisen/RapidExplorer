from data.filetype import FileType


class ZipFileType(FileType):
    NAME = 'zip'
    
    @staticmethod
    def check(filePath: str) -> bool:
        if filePath.endswith('.zip'):
            return True
        return False