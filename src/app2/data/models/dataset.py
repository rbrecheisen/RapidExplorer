from models.fileset import FileSet
from models.file import File


class Dataset:
    def __init__(self, path: str, name: str) -> None:
        self.path = path
        self.name = name
        self.fileSets = []

    def firstFile(self) -> File:
        if len(self.fileSets) > 0:
            return self.fileSets[0].firstFile()
        return None
    
    def firstFileSet(self) -> FileSet:
        if len(self.fileSets) > 0:
            return self.fileSets[0]
        return None
        
    def __str__(self) -> str:
        s = f'Dataset(name={self.name}, path={self.path}):\n'
        for fileSet in self.fileSets:
            s += str(fileSet) + '\n'
        return s
