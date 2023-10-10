import utilities

from models.file import File


class FileSet:
    def __init__(self, path: str, name: str=None) -> None:
        self._path = path
        self._name = name
        if not self._name:
            self._name = utilities.create_random_name('fileset')
        self._files = []

    def nrFiles(self) -> int:
        return len(self._files)
        
    def firstFile(self) -> File:
        if self.nrFiles() > 0:
            return self._files[0]
        return None
    
    def __str__(self) -> str:
        s = f'  FileSet(name={self._name}, path={self._path}):\n'
        for f in self._files:
            s += str(f) + '\n'
        return s
