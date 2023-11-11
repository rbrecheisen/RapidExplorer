import pydicom
import pydicom.errors

from data.filetype import FileType


class DicomFileType(FileType):
    def check(self, path: str) -> bool:
        try:
            pydicom.dcmread(path, stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError:
            return False