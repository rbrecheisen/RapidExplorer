import utilities

from typing import List
from fileset import FileSet
from file import File


class Dataset:
    def __init__(self, path: str, name: str=None) -> None:
        self._path = path
        self._name = name
        if not self._name:
            self._name = utilities.create_random_name('dataset')
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
