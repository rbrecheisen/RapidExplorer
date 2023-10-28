from sqlalchemy.orm import Session

from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.multifileset.multifilesetregistrationhelper import MultiFileSetRegistrationHelper
from rapidx.app.data.multifileset.dicommultifilesetfactory import DicomMultiFileSetFactory


class DicomMultiFileSetImporter(Importer):
    def __init__(self, name: str, path: str, session: Session) -> None:
        super(DicomMultiFileSetImporter, self).__init__(name=name, path=path, session=session)

    def run(self):    
        helper = MultiFileSetRegistrationHelper(name=self.name(), path=self.path(), session=self.session())
        multiFileSetModel = helper.execute()
        dicomMultiFileSet = DicomMultiFileSetFactory.create(multiFileSetModel=multiFileSetModel, session=self.session())
        cache = FileCache()
        for dicomFileSet in dicomMultiFileSet:
            for dicomFile in dicomFileSet:
                cache.add(file=dicomFile)
        self.setData(multiFileSetModel)
        self.signal().progress.emit(100)
        self.signal().finished.emit(True)