import os
import pydicom
import pydicom.errors

from PySide6.QtCore import QRunnable

from rapidx.app.dataset import Dataset
from rapidx.app.dicomfileset import DicomFileSet
from rapidx.app.dicomfile import DicomFile
from rapidx.app.datasetstoragemanager import DatasetStorageManager
from rapidx.app.importerprogresssignal import ImporterProgressSignal


class DicomDatasetImporter(QRunnable):
    def __init__(self, path: str) -> None:
        super(DicomDatasetImporter, self).__init__()
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
        data = {}
        nrFiles = 0
        for root, dirs, files in os.walk(self.path()):
            for fileName in files:
                filePath = os.path.join(root, fileName)
                try:
                    pydicom.dcmread(filePath, stop_before_pixels=True)
                    if root not in data.keys():
                        data[root] = []
                    data[root].append(filePath)
                    nrFiles += 1
                except pydicom.errors.InvalidDicomError:
                    print(f'File {fileName} is not a valid DICOM file')
                    continue
        i = 0
        for fileSetPath in data.keys():
            fileSetName = os.path.relpath(fileSetPath, self.path())
            fileSet = DicomFileSet(path=fileSetPath, name=fileSetName)
            for filePath in data[fileSetPath]:
                p = pydicom.dcmread(filePath)
                p.decompress('pylibjpeg')
                file = DicomFile(path=filePath, data=p)
                fileSet.addFile(file)
                progress = int((i + 1) / nrFiles * 100)
                self.signal().progress.emit(progress)
                i += 1
            fileSet.sortByInstanceNumber()
            self.data().addFileSet(fileSet)
        manager = DatasetStorageManager()
        manager.save(self.data())
        self.signal().done.emit(True)
