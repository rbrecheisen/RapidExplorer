from data.filetype import FileType
from data.dicomfiletype import DicomFileType
from data.pngfiletype import PngFileType
from data.jpegfiletype import JpegFileType


class FileTypeFactory:
    @staticmethod
    def forName(name: str) -> FileType:
        if name == 'dicom':
            return DicomFileType()
        if name == 'png':
            return PngFileType()
        if name == 'jpg':
            return JpegFileType()
        else:
            return None