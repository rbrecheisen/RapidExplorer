from rapidx.app.data.db.db import Db
from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.multifileset.multifilesetregistrationhelper import MultiFileSetRegistrationHelper
from rapidx.app.data.multifileset.dicommultifilesetloader import DicomMultiFileSetLoader
from rapidx.app.utils import create_random_name


class DicomMultiFileSetImporter(Importer):
    def __init__(self, path: str, db=None) -> None:
        name = create_random_name('multifileset')
        super(DicomMultiFileSetImporter, self).__init__(name=name, path=path, db=db)

    def run(self):    

        helper = MultiFileSetRegistrationHelper(name=self.name(), path=self.path(), db=self.db())
        multiFileSetModel = helper.execute()
        self.setData(multiFileSetModel)
        
        loader = DicomMultiFileSetLoader()
        loader.signal().progress.connect(self._updateProgress)
        loader.signal().finished.connect(self._importFinished)
        dicomMultiFileSet = loader.execute(multiFileSetModel=multiFileSetModel, db=self.db())

        cache = FileCache()
        for dicomFileSet in dicomMultiFileSet:
            for dicomFile in dicomFileSet:
                cache.add(file=dicomFile)

    def _updateProgress(self, progress) -> None:
        self.signal().progress.emit(progress)

    def _importFinished(self, value) -> None:
        self.signal().finished.emit(value)