import pydicom
import pydicom.errors

from data.filetype import FileType


class DicomFileType(FileType):
    NAME = 'dicom'
    
    @staticmethod
    def check(filePath: str) -> bool:
        if filePath.endswith('.dcm'):
            return True
        try:
            pydicom.dcmread(filePath, stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError:
            pass
        return False