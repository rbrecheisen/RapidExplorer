from data.filetype import FileType


class CsvFileType(FileType):
    NAME = 'csv'
    
    @staticmethod
    def check(filePath: str) -> bool:
        if filePath.endswith('.csv'):
            return True
        return False