from typing import List
from models.loaded.loadedfile import LoadedFile


class LoadedFileSet:
    def __init__(self) -> None:
        self.files = []

    def getFile(self) -> List[LoadedFile]:
        return self.files
    
    def addFile(self, f) -> None:
        self.files.append(f)