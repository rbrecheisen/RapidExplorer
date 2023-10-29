from rapidx.app.data.db import Db
from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.dicomfilefactory import DicomFileFactory
from rapidx.app.data.file.fileregistrationhelper import FileRegistrationHelper


class DicomFileImporter(Importer):
    def __init__(self, path: str, db: Db) -> None:
        super(DicomFileImporter, self).__init__(name=None, path=path, db=db)

    def run(self) -> None:
        helper = FileRegistrationHelper(path=self.path(), db=self.db())
        multiFileSetModel = helper.execute()
        fileModel = multiFileSetModel.firstFileSetModel().firstFileModel()
        # TODO: Send progress signals from factory!
        # Use event listener?
        dicomFile = DicomFileFactory.create(fileModel=fileModel)
        cache = FileCache()
        cache.add(file=dicomFile)
        self.setData(multiFileSetModel)
        self.signal().progress.emit(100)
        self.signal().finished.emit(True)
