from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.file.dicomfile import DicomFile


class DicomFileFactory:
    @staticmethod
    def create(fileModel: FileModel) -> DicomFile:
        return DicomFile(fileModel=fileModel)
