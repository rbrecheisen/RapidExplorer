from rapidx.app.data.db import Db
from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.fileset.filesetregistrationhelper import FileSetRegistrationHelper
from rapidx.app.data.fileset.dicomfilesetfactory import DicomFileSetFactory
from rapidx.app.utils import create_random_name


class DicomFileSetImporter(Importer):
    def __init__(self, path: str, db: Db) -> None:
        name = create_random_name('fileset')
        super(DicomFileSetImporter, self).__init__(name=name, path=path, db=db)
    
    def run(self) -> None:    
        helper = FileSetRegistrationHelper(name=self.name(), path=self.path(), db=self.db())
        multiFileSetModel = helper.execute()
        fileSetModel = multiFileSetModel.firstFileSetModel()
        factory = DicomFileSetFactory()
        factory.signal().progress.connect(self._updateProgress)
        dicomFileSet = factory.create(fileSetModel=fileSetModel, db=self.db())
        cache = FileCache()
        for dicomFile in dicomFileSet:
            cache.add(file=dicomFile)
        self.setData(multiFileSetModel)

    def _updateProgress(self, progress) -> None:
        self.signal().progress.emit(progress)