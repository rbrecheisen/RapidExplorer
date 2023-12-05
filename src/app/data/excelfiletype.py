from data.filetype import FileType


class ExcelFileType(FileType):
    @staticmethod
    def check(filePath: str) -> bool:
        if filePath.endswith('.xls') or filePath.endswith('.xlsx'):
            return True
        return False