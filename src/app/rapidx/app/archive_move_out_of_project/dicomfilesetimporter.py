import os
import pydicom
import pydicom.errors

from PySide6.QtCore import QRunnable

from rapidx.app.dataset import Dataset
from rapidx.app.dicomfileset import DicomFileSet
from rapidx.app.dicomfile import DicomFile
from rapidx.app.datasetstoragemanager import DatasetStorageManager
from rapidx.app.importerprogresssignal import ImporterProgressSignal


class DicomFileSetImporter(QRunnable):
    def __init__(self, path: str) -> None:
        super(DicomFileSetImporter, self).__init__()
        self._path = path
        self._data = Dataset()
        self._signal = ImporterProgressSignal() 

    def path(self) -> str:
        return self._path

    def data(self) -> Dataset:
        return self._data
    
    def signal(self) -> ImporterProgressSignal:
        return self._signal

    def run(self):
        fileSet = DicomFileSet(path=self.path())
        files = os.listdir(self.path())
        nrFiles = len(files)
        i = 0
        for f in files:
            fileName = f
            filePath = os.path.join(self.path(), fileName)
            try:
                p = pydicom.dcmread(filePath)
                p.decompress('pylibjpeg')
                file = DicomFile(path=filePath, data=p)
                fileSet.addFile(file)
            except pydicom.errors.InvalidDicomError:
                print(f'File {fileName} is not a valid DICOM file')
                continue
            progress = int((i + 1) / nrFiles * 100)
            i += 1
            self.signal().progress.emit(progress)
        fileSet.sortByInstanceNumber()
        self.data().addFileSet(fileSet)
        manager = DatasetStorageManager()
        manager.save(self.data())
        self.signal().done.emit(True)