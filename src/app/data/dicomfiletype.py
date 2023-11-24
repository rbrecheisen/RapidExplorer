import os
import pydicom
import pydicom.errors

from data.filetype import FileType
from data.dicomfile import DicomFile
from data.registeredfilemodel import RegisteredFileModel


class DicomFileType(FileType):
    name = 'dicom'

    def __init__(self) -> None:
        super(DicomFileType, self).__init__()

    def check(self, path: str) -> bool:
        try:
            pydicom.dcmread(path, stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError as e:
            if os.path.splitext(path)[1] == '' or path.endswith('.dcm'):
                print(f'{path} is not a valid DICOM file ({e})')
            return False
        
    def read(self, registeredFileModel: RegisteredFileModel) -> DicomFile:
        return DicomFile(registeredFileModel=registeredFileModel)
