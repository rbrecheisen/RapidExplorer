import utilities

from models.fileset import FileSet
from models.file import File


class Dataset:
    def __init__(self, path: str, name: str=None) -> None:
        self._path = path
        self._name = name
        if not self._name:
            self._name = utilities.create_random_name('dataset')
        self._fileSets = []

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
        s = f'Dataset(name={self._name}, path={self._path}):\n'
        for fileSet in self._fileSets:
            s += str(fileSet) + '\n'
        return s
