from rapidx.app.data.db.db import Db
from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.multifileset.multifilesetregistrationhelper import MultiFileSetRegistrationHelper
from rapidx.app.data.multifileset.dicommultifilesetloader import DicomMultiFileSetLoader
from rapidx.app.utils import create_random_name


class DicomMultiFileSetImporter(Importer):
    def __init__(self, path: str, db: Db) -> None:
        name = create_random_name('multifileset')
        super(DicomMultiFileSetImporter, self).__init__(name=name, path=path, db=db)

    def run(self):    
        # This helper also counts the total nr. of files
        helper = MultiFileSetRegistrationHelper(name=self.name(), path=self.path(), db=self.db())
        multiFileSetModel = helper.execute()
        # Set data here and not after import finished signal is triggered
        self.setData(multiFileSetModel)

        # The multi-fileset loader has to know the total nr. of files. Otherwise
        # it cannot calculate progress
        loader = DicomMultiFileSetLoader(multiFileSetModel=multiFileSetModel, db=self._db)
        loader.signal().progress.connect(self._updateProgress)
        # loader.signal().finished.connect(self._importFinished)
        dicomMultiFileSet = loader.execute()
        cache = FileCache()
        for dicomFileSet in dicomMultiFileSet:
            for dicomFile in dicomFileSet:
                cache.add(file=dicomFile)
        self.signal().finished.emit(True)

    def _updateProgress(self, progress) -> None:
        print(f'DicomMultiFileSetImporter.progress = {progress}')
        self.signal().progress.emit(progress)

    def _importFinished(self, value) -> None:
        self.signal().finished.emit(value)