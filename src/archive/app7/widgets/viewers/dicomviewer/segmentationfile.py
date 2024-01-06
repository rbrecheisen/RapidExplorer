import numpy as np


class SegmentationFile:
    def __init__(self, filePath: str) -> None:
        self._filePath = filePath
        self._data = np.load(self._filePath)

    def filePath(self) -> str:
        return self._filePath
    
    def data(self) -> np.array:
        return self._data