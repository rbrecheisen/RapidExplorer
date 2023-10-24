from sqlalchemy.orm import Session

from rapidx.tests.data.importer import Importer
from rapidx.tests.data.filecache import FileCache
from rapidx.tests.data.file.dicomfilefactory import DicomFileFactory
from rapidx.tests.data.file.fileregistrationhelper import FileRegistrationHelper


class DicomFileImporter(Importer):
    def __init__(self, path: str, session: Session) -> None:
        super(DicomFileImporter, self).__init__(path=path, session=session)

    def execute(self) -> None:
        # Register file in SQL database
        helper = FileRegistrationHelper(path=self.path(), session=self.session())
        multiFileSetModel = helper.execute()
        fileModel = multiFileSetModel.firstFileSetModel().firstFileModel()
        # Create new DicomFile object with physical data
        dicomFile = DicomFileFactory.create(fileModel=fileModel)
        self.setData(dicomFile)
        # Store DicomFile object in FileCache
        cache = FileCache()
        cache.add(file=dicomFile)
        # Notify listeners that we're finished
        self.signal().progress.emit(100)
        self.signal().done.emit(True)
