from data.filetype import FileType


class PngFileType(FileType):
    NAME = 'png'
    
    @staticmethod
    def check(filePath: str) -> bool:
        if filePath.endswith('.png'):
            return True
        return False