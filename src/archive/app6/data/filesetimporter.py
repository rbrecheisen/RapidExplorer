from data.importer import Importer
from data.filesetregistrar import FileSetRegistrar
from data.registeredmultifilesetcontentloader import RegisteredMultiFileSetContentLoader
from data.filetype import FileType


class FileSetImporter(Importer):
    def __init__(self, path: str, fileType: FileType) -> None:
        super(FileSetImporter, self).__init__(path=path, fileType=fileType)
    
    def run(self):
        registrar = FileSetRegistrar(path=self.path(), fileType=self.fileType())
        registeredMultiFileSetModel = registrar.execute()
        loader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel)
        loader.signal().progress.connect(self._updateImportProgress)
        data = loader.execute()
        self.setData(data)

    def _updateImportProgress(self, progress):
        self.signal().progress.emit(progress)