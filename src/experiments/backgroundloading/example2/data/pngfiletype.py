from data.filetype import FileType


class PngFileType(FileType):
    def check(self, path: str) -> bool:
        if path.endswith('.png'):
            return True
        return False