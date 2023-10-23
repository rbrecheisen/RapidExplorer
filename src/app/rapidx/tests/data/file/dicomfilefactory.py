from rapidx.tests.data.file.filemodel import FileModel
from rapidx.tests.data.file.dicomfile import DicomFile


class DicomFileFactory:
    @staticmethod
    def create(fileModel: FileModel) -> DicomFile:
        return DicomFile(fileModel=fileModel)
