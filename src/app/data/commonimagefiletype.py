from data.filetype import FileType
from data.pngfiletype import PngFileType
from data.jpegfiletype import JpegFileType


class CommonImageFileType(FileType):
    name = 'png/jpeg'

    def __init__(self) -> None:
        super(CommonImageFileType, self).__init__()
        
    def check(self, path: str) -> bool:
        pngFileType = PngFileType()
        jpegFileType = JpegFileType()
        if pngFileType.check(path) or jpegFileType.check(path):
            return True
        return False