import pydicom

from models.loaded.loadedfile import LoadedFile


class LoadedDicomImage(LoadedFile):
    def __init__(self, p: pydicom.FileDataset) -> None:
        self.p = p