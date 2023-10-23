from sqlalchemy.orm import Session
from PySide6.QtCore import QRunnable

from rapidx.tests.data.file.dicomfile import DicomFile
from rapidx.tests.data.file.dicomfilefactory import DicomFileFactory
from rapidx.tests.data.file.fileregistrationhelper import FileRegistrationHelper
from rapidx.tests.data.progresssignal import ProgressSignal


class DicomFileImporter(QRunnable):
    # TODO: inherit from base class Importer(QRunnable)!
    def __init__(self, path: str, session: Session) -> None:
        self._path = path
        self._session = session
        self._data = None
        self._signal = ProgressSignal()

    def path(self) -> str:
        return self._path
    
    def session(self) -> Session:
        return self._session
    
    def data(self) -> DicomFile:
        return self._data
    
    def setData(self, data: DicomFile) -> None:
        self._data = data

    def signal(self) -> ProgressSignal:
        return self._signal
    
    def execute(self) -> None:
        helper = FileRegistrationHelper(path=self.path(), session=self.session())
        multiFileSetModel = helper.execute()
        fileModel = multiFileSetModel.firstFileSetModel().firstFileModel()
        dicomFile = DicomFileFactory.create(fileModel=fileModel)
        self.setData(dicomFile)
        self.signal().progress.emit(100)
        self.signal().done.emit(True)
