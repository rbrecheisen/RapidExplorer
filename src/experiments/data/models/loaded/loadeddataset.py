from typing import List

from models.loaded.loadedfileset import LoadedFileSet


class LoadedDataset:
    def __init__(self) -> None:
        self.fileSets = []

    def getFileSet(self) -> List[LoadedFileSet]:
        return self.fileSets

    def addFileSet(self, fileSet: LoadedFileSet) -> None:
        self.fileSets.append(fileSet)