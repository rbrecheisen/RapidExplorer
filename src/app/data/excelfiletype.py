from data.filetype import FileType


class ExcelFileType(FileType):
    NAME = 'excel'
    
    @staticmethod
    def check(filePath: str) -> bool:
        if filePath.endswith('.xls') or filePath.endswith('.xlsx'):
            return True
        return False