from rapidx.app.data.db.db import Db
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.file.dicomfile import DicomFile
from rapidx.app.data.loader import Loader


class DicomFileLoader(Loader):
    def __init__(self, fileModel: FileModel, db: Db) -> None:
        super(DicomFileLoader, self).__init__()
        self._fileModel = fileModel
        self._db = db

    def execute(self) -> DicomFile:
        dicomFile = DicomFile(fileModel=self._fileModel)
        self.signal().progress.emit(1)
        self.signal().finished.emit(True)
        return dicomFile
