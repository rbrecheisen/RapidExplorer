import utilities

from typing import List
from models.file import File


class FileSet:
    def __init__(self, path: str, name: str=None) -> None:
        self._path = path
        self._name = name
        if not self._name:
            self._name = utilities.create_random_name('fileset')
        self._files = []

    def path(self) -> str:
        return self._path
    
    def name(self) -> str:
        return self._name

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
    
    def sortByInstanceNumber(self) -> None:
        self.files().sort(key=lambda p: int(p.data().InstanceNumber))
