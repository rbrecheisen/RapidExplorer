from sqlalchemy.orm import Session

from rapidx.app.data.importer import Importer
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.fileset.filesetregistrationhelper import FileSetRegistrationHelper
from rapidx.app.data.fileset.dicomfilesetfactory import DicomFileSetFactory


class DicomFileSetImporter(Importer):
    def __init__(self, name: str, path: str, session: Session) -> None:
        super(DicomFileSetImporter, self).__init__(name=name, path=path, session=session)

    def execute(self):    
        # TODO: How to deal with progress updates across these different classes?
        # Use event listener based on signals! Can we just pass the signal from 
        # DicomFileSetImporter to the helper classes?
        helper = FileSetRegistrationHelper(name=self.name(), path=self.path(), session=self.session())
        multiFileSetModel = helper.execute()
        fileSetModel = multiFileSetModel.firstFileSetModel()
        # This step is the most time-consuming (good candidate for progress bar updates). 
        dicomFileSet = DicomFileSetFactory.create(fileSetModel=fileSetModel, session=self.session())
        cache = FileCache()
        for dicomFile in dicomFileSet:
            cache.add(file=dicomFile)
        self.setData(dicomFileSet)
        self.signal().progress.emit(100)
        self.signal().done.emit(True)
