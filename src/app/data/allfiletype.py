import os

from data.filetype import FileType
from data.pathfile import PathFile
from data.registeredfilemodel import RegisteredFileModel


class AllFileType(FileType):
    name = 'all'
    
    def check(self, path: str) -> bool:
        return os.path.isfile(path)
    
    def read(self, registeredFileModel: RegisteredFileModel) -> PathFile:
        # Since we do not know what kind of file this is, we store it as 
        # path file, i.e., a file object for the cache that just contains
        # the path
        return PathFile(registeredFileModel)