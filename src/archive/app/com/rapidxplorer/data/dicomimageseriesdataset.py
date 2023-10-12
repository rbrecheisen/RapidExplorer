import os
import pydicom

from com.rapidxplorer.data.imagedataset import ImageDataset


class DicomImageSeriesDataset(ImageDataset):

    def __init__(self) -> None:
        super(DicomImageSeriesDataset, self).__init__()

    def load(self, path: str) -> None:
        images = [pydicom.dcmread(os.path.join(path, f)) for f in os.listdir(path)]
        [p.decompress('pylibjpeg') for p in images]
        images.sort(key=lambda p: int(p.InstanceNumber))
        self._data = {path: images}

    def series(self) -> []:
        if len(self._data.keys()) > 0:
            first_key = list(self._data.keys())[0]
            return self._data[first_key]
        return None
    
    def image(self, index):
        series = self.series()
        if series and len(series) > index:
            return series[index]
        return None
