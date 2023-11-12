from data.filetype import FileType


class AllFileType(FileType):
    def check(self, path: str) -> bool:
        return True