import pydicom

from PySide6.QtCore import QRunnable

from app.dataset import Dataset
from app.fileset import FileSet
from app.dicomfile import DicomFile
from app.datasetstoragemanager import DatasetStorageManager
from app.importerprogresssignal import ImporterProgressSignal


class DicomFileImporter(QRunnable):
    def __init__(self, path: str) -> None:
        super(DicomFileImporter, self).__init__()
        self._path = path
        self._data = Dataset(path=None)
        self._signal = ImporterProgressSignal()

    def path(self) -> str:
        return self._path

    def data(self) -> Dataset:
        return self._data
    
    def signal(self) -> ImporterProgressSignal:
        return self._signal

    def run(self):
        p = pydicom.dcmread(self.path())
        p.decompress('pylibjpeg')
        file = DicomFile(path=self.path(), data=p)
        fileSet = FileSet(path=None)
        fileSet.addFile(file)
        self.data().addFileSet(fileSet)
        manager = DatasetStorageManager()
        manager.save(self.data())
        self.signal().progress.emit(100)
        self.signal().done.emit(True)
