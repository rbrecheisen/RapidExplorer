from data.importer import Importer
from data.multifilesetregistrar import MultiFileSetRegistrar
from data.registeredmultifilesetcontentloader import RegisteredMultiFileSetContentLoader
from data.filetype import FileType


class MultiFileSetImporter(Importer):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(MultiFileSetImporter, self).__init__(path=path, fileType=fileType)
        self._i = 0
        self._progess = 0

    def run(self):
        registrar = MultiFileSetRegistrar(path=self.path(), fileType=self.fileType())
        registeredMultiFileSetModel = registrar.execute()
        loader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel, fileType=self.fileType())
        loader.signal().progress.connect(self._updateLoaderProgress)
        data = loader.execute()
        self.setData(data)

    def _updateLoaderProgress(self, progress):
        # TODO: Think carefully about this passing on of signals all over the place!
        pass
