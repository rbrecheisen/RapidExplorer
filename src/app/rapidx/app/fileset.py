from typing import List

from rapidx.app.file import File
from rapidx.app.utilities import create_random_name


class FileSet:
    def __init__(self, name: str=None, path: str=None) -> None:
        self._id = None
        self._datasetId = None
        self._name = name
        if not self._name:
            self._name = create_random_name('fileset')
        self._path = path
        self._files = []

    def id(self) -> int:
        return self._id
    
    def setId(self, id) -> None:
        self._id = id

    def datasetId(self) -> None:
        return self._datasetId

    def setDatasetId(self, datasetId: int) -> None:
        self._datasetId = datasetId

    def path(self) -> str:
        return self._path
    
    def name(self) -> str:
        return self._name
    
    def setName(self, name: str) -> None:
        self._name = name

    def files(self) -> List[str]:
        return self._files

    def addFile(self, f) -> None:
        self.files().append(f)

    def nrFiles(self) -> int:
        return len(self.files())
        
    def firstFile(self) -> File:
        if self.nrFiles() > 0:
            return self.files()[0]
        return None
    
    def __str__(self) -> str:
        return f'FileSet(name={self.name()}, path={self.path()}, nrFiles={self.nrFiles()})'