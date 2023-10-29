from rapidx.app.data.db import Db
from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.fileset.filesetregistrationhelper import FileSetRegistrationHelper
from rapidx.app.data.fileset.dicomfilesetfactory import DicomFileSetFactory


class DicomFileSetImporter(Importer):
    def __init__(self, name: str, path: str, db: Db) -> None:
        super(DicomFileSetImporter, self).__init__(name=name, path=path, db=db)
    
    def run(self) -> None:    
        helper = FileSetRegistrationHelper(name=self.name(), path=self.path(), db=self.db())
        multiFileSetModel = helper.execute()
        fileSetModel = multiFileSetModel.firstFileSetModel()
        dicomFileSet = DicomFileSetFactory.create(fileSetModel=fileSetModel, db=self.db())
        cache = FileCache()
        for dicomFile in dicomFileSet:
            cache.add(file=dicomFile)
        # self.setData(dicomFileSet)  # TODO: Add MultiFileSetModel here?
        self.setData(multiFileSetModel)
        self.signal().progress.emit(100)
        self.signal().finished.emit(True)
