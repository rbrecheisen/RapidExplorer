from rapidx.app.data.db import Db
from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.multifileset.multifilesetregistrationhelper import MultiFileSetRegistrationHelper
from rapidx.app.data.multifileset.dicommultifilesetfactory import DicomMultiFileSetFactory
from rapidx.app.utils import create_random_name


class DicomMultiFileSetImporter(Importer):
    def __init__(self, path: str, db: Db) -> None:
        name = create_random_name('multifileset')
        super(DicomMultiFileSetImporter, self).__init__(name=name, path=path, db=db)

    def run(self):    
        helper = MultiFileSetRegistrationHelper(name=self.name(), path=self.path(), db=self.db())
        multiFileSetModel = helper.execute()
        factory = DicomMultiFileSetFactory()
        factory.signal().progress.connect(self._updateProgress)
        dicomMultiFileSet = factory.create(multiFileSetModel=multiFileSetModel, db=self.db())
        cache = FileCache()
        for dicomFileSet in dicomMultiFileSet:
            for dicomFile in dicomFileSet:
                cache.add(file=dicomFile)
        self.setData(multiFileSetModel)

    def _updateProgress(self, progress) -> None:
        self.signal().progress.emit(progress)