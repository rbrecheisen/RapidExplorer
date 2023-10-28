from sqlalchemy.orm import Session

from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.dicomfilefactory import DicomFileFactory
from rapidx.app.data.file.fileregistrationhelper import FileRegistrationHelper


class DicomFileImporter(Importer):
    def __init__(self, path: str, session: Session) -> None:
        super(DicomFileImporter, self).__init__(name=None, path=path, session=session)

    def run(self) -> None:
        helper = FileRegistrationHelper(path=self.path(), session=self.session())
        multiFileSetModel = helper.execute()
        fileModel = multiFileSetModel.firstFileSetModel().firstFileModel()
        dicomFile = DicomFileFactory.create(fileModel=fileModel)
        cache = FileCache()
        cache.add(file=dicomFile)
        self.setData(multiFileSetModel)
        self.signal().progress.emit(100)
        self.signal().finished.emit(True)
