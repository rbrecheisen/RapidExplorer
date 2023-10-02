from com.application.dataset.imagedataset import ImageDataset


class DicomImageSeriesDataset(ImageDataset):

    def __init__(self) -> None:
        self._dicomImages = []

    def load(self, path: str) -> None:
        pass

    def dicomImages(self) -> []:
        return self._dicomImages