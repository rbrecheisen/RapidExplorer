from data.filetype import FileType


class CsvFileType(FileType):
    @staticmethod
    def check(filePath: str) -> bool:
        if filePath.endswith('.csv'):
            return True
        return False