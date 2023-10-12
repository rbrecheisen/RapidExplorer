import os
import pydicom
import pydicom.errors

from PySide6.QtCore import QRunnable

from dataset import Dataset
from fileset import FileSet
from dicomfile import DicomFile
from importerprogresssignal import ImporterProgressSignal


class DicomFileSetImporter(QRunnable):
    def __init__(self, path: str) -> None:
        super(DicomFileSetImporter, self).__init__()
        self._path = path
        self._data = Dataset(path=path)
        self._signal = ImporterProgressSignal() 

    def path(self) -> str:
        return self._path

    def data(self) -> Dataset:
        return self._data
    
    def signal(self) -> ImporterProgressSignal:
        return self._signal

    def run(self):
        fileSet = FileSet(path=self.path())
        files = os.listdir(self.path())
        nrFiles = len(files)
        i = 0
        for f in files:
            fileName = f
            filePath = os.path.join(self.path(), fileName)
            try:
                p = pydicom.dcmread(filePath)
                p.decompress('pylibjpeg')
                file = DicomFile(path=self.path(), data=p)
                fileSet.addFile(file)
            except pydicom.errors.InvalidDicomError:
                print(f'File {fileName} is not a valid DICOM file')
                continue
            progress = int((i + 1) / nrFiles * 100)
            i += 1
            self.signal().progress.emit(progress)
        fileSet.sortByInstanceNumber()
        self.data().addFileSet(fileSet)
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
 