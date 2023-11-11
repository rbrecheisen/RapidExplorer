from data.filetype import FileType


class TextFileType(FileType):
    def check(self, path: str) -> bool:
        if path.endswith('.txt'):
            return True
        return False