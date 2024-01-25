from typing import Any

from mosamaticdesktop.data.file import File


class FileContent:
    def __init__(self, file: File, fileObject: Any) -> None:
        self._file = file
        self._fileObject = fileObject

    def file(self) -> File:
        return self._file

    def fileObject(self) -> Any:
        return self._fileObject
    
    def id(self) -> str:
        return self._file.id()