from data.importer import Importer
from data.fileregistrar import FileRegistrar
from data.registeredmultifilesetcontentloader import RegisteredMultiFileSetContentLoader
from data.filetype import FileType


class FileImporter(Importer):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(FileImporter, self).__init__(path=path, fileType=fileType)
        self._i = 0
        self._progress = 0

    def run(self):
        # Always register a new file even if it was already registered (and loaded) for
        # another multi-fileset. This will result in a new file ID so a new addition
        # to the file cache as well. This is ok.
        registrar = FileRegistrar(path=self.path(), fileType=self.fileType())
        registeredMultiFileSetModel = registrar.execute()

        # Load the file contents for this multi-fileset model. 
        loader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel, fileType=self.fileType())
        loader.signal().progress.connect(self._updateLoaderProgress)
        data = loader.execute()
        self.setData(data)

    def _updateLoaderProgress(self, progress):
        # TODO: Think carefully about this passing on of signals all over the place!
        pass
