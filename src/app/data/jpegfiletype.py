from data.filetype import FileType


class JpegFileType(FileType):
    NAME = 'jpeg'
    
    @staticmethod
    def check(filePath: str) -> bool:
        if filePath.endswith('.jpg') or filePath.endswith('.jpeg'):
            return True
        return False