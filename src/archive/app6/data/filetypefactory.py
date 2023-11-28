from data.filetype import FileType
from data.dicomfiletype import DicomFileType
from data.pngfiletype import PngFileType
from data.jpegfiletype import JpegFileType
from data.allfiletype import AllFileType


class FileTypeFactory:
    @staticmethod
    def forName(name: str) -> FileType:
        if name == 'dicom':
            return DicomFileType()
        elif name == 'png':
            return PngFileType()
        elif name == 'jpg':
            return JpegFileType()
        elif name == 'all':
            return AllFileType()
        else:
            return None