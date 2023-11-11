from utils import create_random_name
from data.registrar import Registrar
from data.dataregistry import DataRegistry
from data.multifilesetmodel import MultiFileSetModel
from data.filetype import FileType


class MultiFileSetRegistrar(Registrar):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(MultiFileSetRegistrar, self).__init__()
        self._path = path
        self._fileType = fileType

    def execute(self) -> MultiFileSetModel:
        registry = DataRegistry()
        registeredMultiFileSetModel = registry.registerMultiFileSetModelForMultiFileSet(self._path, self._fileType)
        return registeredMultiFileSetModel
