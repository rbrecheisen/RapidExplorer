from typing import List

from data.fileset import FileSet


class TaskOutput:
    def __init__(self, fileSet: FileSet, errorInfo: List[str]=None) -> None:
        self._fileSet = fileSet
        self._errorInfo = errorInfo

    def fileSet(self) -> FileSet:
        return self._fileSet
    
    def errorInfo(self) -> List[str]:
        return self._errorInfo