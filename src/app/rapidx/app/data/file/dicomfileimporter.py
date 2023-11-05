from rapidx.app.data.db.db import Db
from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.dicomfilefactory import DicomFileFactory
from rapidx.app.data.file.fileregistrationhelper import FileRegistrationHelper


class DicomFileImporter(Importer):
    def __init__(self, path: str, db: Db=None) -> None:
        super(DicomFileImporter, self).__init__(name=None, path=path, db=db)

    def run(self) -> None:
        helper = FileRegistrationHelper(path=self.path(), db=self.db())
        multiFileSetModel = helper.execute()
        self.setData(multiFileSetModel)
        fileModel = multiFileSetModel.firstFileSetModel().firstFileModel()
        factory = DicomFileFactory()
        factory.signal().progress.connect(self._updateProgress)
        factory.signal().finished.connect(self._importFinished)
        dicomFile = factory.create(fileModel=fileModel)
        cache = FileCache()
        cache.add(file=dicomFile)

    def _updateProgress(self, progress) -> None:
        self.signal().progress.emit(progress)

    def _importFinished(self, value) -> None:
        self.signal().finished.emit(value)        
