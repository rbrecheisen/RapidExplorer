from data.importer import Importer
from data.filesetregistrar import FileSetRegistrar
from data.registeredmultifilesetcontentloader import RegisteredMultiFileSetContentLoader
from data.filetype import FileType


class FileSetImporter(Importer):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(FileSetImporter, self).__init__(path=path, fileType=fileType)
        self._i = 0
        self._progess = 0
    
    def run(self):
        registrar = FileSetRegistrar(path=self.path(), fileType=self.fileType())
        registeredMultiFileSetModel = registrar.execute()
        loader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel, fileType=self.fileType())
        loader.signal().progress.connect(self._updateLoaderProgress)
        data = loader.execute()
        self.setData(data)

    def _updateLoaderProgress(self, progress):
        # TODO: Think carefully about this passing on of signals all over the place!
        pass
