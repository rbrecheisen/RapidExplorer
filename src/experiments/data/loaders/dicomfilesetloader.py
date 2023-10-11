import pydicom

from typing import List, Dict
from PySide6.QtCore import QRunnable
from models.dataset import Dataset
from models.fileset import FileSet
from signals.loaderprogresssignal import LoaderProgressSignal


class DicomFileSetLoader(QRunnable):
    def __init__(self, path: str) -> None:
        super(DicomFileSetLoader, self).__init__()
        self._path = path
        self._data = Dataset(path=path)
        self._signal = LoaderProgressSignal()

    def path(self) -> str:
        return self._path

    def data(self) -> Dataset:
        return self._data
    
    def signal(self) -> LoaderProgressSignal:
        return self._signal

    def run(self):
        # Bla
        file = DicomFile(path=self.path(), data=p)
        fileSet = FileSet(path=self.path())
        fileSet.addFile(file)
        self.data().addFileSet(fileSet)
        # Emit signals
        self.signal().progress.emit(100)
        self.signal().done.emit(True)




# class DicomFileSetLoader(QRunnable):
#     def __init__(self, dataset: Dataset) -> None:
#         super(DicomFileSetLoader, self).__init__()
#         self._dataset = dataset
#         self._data = {}
#         self._signal = LoaderProgressSignal()

#     def getData(self) -> Dict[str, FileSet]:
#         return self._data
    
#     def getImageSeries(self) -> List[pydicom.FileDataset]:
#         return self._data[list(self._data.keys())[0]]

#     def run(self):
#         fileSet = self._dataset.firstFileSet()
#         i = 0
#         self._data = {fileSet.name: []}
#         for file in fileSet.files:
#             p = pydicom.dcmread(file.path)
#             p.decompress('pylibjpeg')
#             self._data[fileSet.name].append(p)
#             progress = int((i + 1) / fileSet.nrFiles() * 100)
#             self._signal.progress.emit(progress)
#             i += 1
#         self._data[fileSet.name].sort(key=lambda p: int(p.InstanceNumber))
#         self._signal.done.emit(True)
 