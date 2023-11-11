import pydicom
import pydicom.errors

from data.filetype import FileType
from data.dicomfile import DicomFile
from data.registeredfilemodel import RegisteredFileModel


class DicomFileType(FileType):
    @staticmethod
    def check(path: str) -> bool:
        try:
            pydicom.dcmread(path, stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError:
            return False
        
    @staticmethod
    def read(registeredFileModel: RegisteredFileModel) -> DicomFile:
        return DicomFile(registeredFileModel=registeredFileModel)
