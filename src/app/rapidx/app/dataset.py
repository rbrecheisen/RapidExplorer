from typing import List

from rapidx.app.fileset import FileSet
from rapidx.app.file import File
from rapidx.app.utilities import create_random_name


class Dataset:
    def __init__(self, path: str=None, name: str=None) -> None:
        self._path = path
        self._name = name
        if not self._name:
            self._name = create_random_name('dataset')
        self._fileSets = []

    def path(self) -> str:
        return self._path
    
    def name(self) -> str:
        return self._name
    
    def setName(self, name: str) -> None:
        # TODO: also update SQL database object!
        self._name = name

    def fileSets(self) -> List[FileSet]:
        return self._fileSets
    
    def addFileSet(self, fileSet) -> None:
        self.fileSets().append(fileSet)

    def nrFileSets(self) -> int:
        return len(self._fileSets)
    
    def nrFiles(self) -> int:
        total = 0
        for fileSet in self._fileSets:
            total += fileSet.nrFiles()
        return total

    def firstFile(self) -> File:
        if len(self._fileSets) > 0:
            return self._fileSets[0].firstFile()
        return None
    
    def firstFileSet(self) -> FileSet:
        if len(self._fileSets) > 0:
            return self._fileSets[0]
        return None

    def __str__(self) -> str:
        return f'Dataset(name={self.name()}, path={self.path()}, nrFileSets={self.nrFiles()})'