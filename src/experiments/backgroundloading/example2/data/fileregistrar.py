from data.registrar import Registrar
from data.dataregistry import DataRegistry
from data.multifilesetmodel import MultiFileSetModel


class FileRegistrar(Registrar):
    def __init__(self, path: str) -> None:
        self._path = path

    def execute(self) -> MultiFileSetModel:
        registry = DataRegistry()
        registeredMultiFileSetModel = registry.registerMultiFileSetModelFromFilePath(self._path)
        return registeredMultiFileSetModel
