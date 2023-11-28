from data.filetype import FileType


class Registrar:
    def __init__(self, path: str, fileType: FileType) -> None:
        self._path = path
        self._fileType = fileType

    def path(self) -> str:
        return self._path
    
    def fileType(self) -> FileType:
        return self._fileType