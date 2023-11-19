from data.filetype import FileType


class AllFileType(FileType):
    name = 'all'
    
    def check(self, path: str) -> bool:
        return True