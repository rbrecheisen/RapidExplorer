from data.filetype import FileType


class JpegFileType(FileType):
    def check(self, path: str) -> bool:
        if path.endswith('.jpg') or path.endswith('.jpeg'):
            return True
        return False