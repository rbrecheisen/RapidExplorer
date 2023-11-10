from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.file.dicomfile import DicomFile
from rapidx.app.data.loader import Loader


class DicomFileLoader(Loader):
    def __init__(self, fileModel: FileModel) -> None:
        super(DicomFileLoader, self).__init__()
        self._fileModel = fileModel

    def execute(self) -> DicomFile:
        dicomFile = DicomFile(fileModel=self._fileModel)
        self.signal().progress.emit(100)
        self.signal().finished.emit(True)
        return dicomFile
