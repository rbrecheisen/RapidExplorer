from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.file.dicomfile import DicomFile
from rapidx.app.data.factory import Factory


class DicomFileLoader(Factory):
    def __init__(self) -> None:
        super(DicomFileLoader, self).__init__()

    def execute(self, fileModel: FileModel) -> DicomFile:
        dicomFile = DicomFile(fileModel=fileModel)
        self.signal().progress.emit(100)
        self.signal().finished.emit(True)
        return dicomFile
