from sqlalchemy.orm import Session

from rapidx.tests.data.importer import Importer
from rapidx.tests.data.filecache import FileCache
from rapidx.tests.data.multifileset.multifilesetregistrationhelper import MultiFileSetRegistrationHelper
from rapidx.tests.data.fileset.dicomfilesetfactory import DicomFileSetFactory


class DicomMultiFileSetImporter(Importer):
    def __init__(self, name: str, path: str, session: Session) -> None:
        super(DicomMultiFileSetImporter, self).__init__(name=name, path=path, session=session)

    def execute(self):    
        helper = MultiFileSetRegistrationHelper(name=self.name(), path=self.path(), session=self.session())
        # # TODO: How to deal with progress updates across these different classes?
        # # Use event listener based on signals! Can we just pass the signal from 
        # # DicomFileSetImporter to the helper classes?
        # helper = FileSetRegistrationHelper(name=self.name(), path=self.path(), session=self.session())
        # multiFileSetModel = helper.execute()
        # fileSetModel = multiFileSetModel.firstFileSetModel()
        # # This step is the most time-consuming (good candidate for progress bar updates). 
        # dicomFileSet = DicomFileSetFactory.create(fileSetModel=fileSetModel, session=self.session())
        # self.setData(dicomFileSet)
        # cache = FileCache()
        # for dicomFile in dicomFileSet:
        #     cache.add(file=dicomFile)
        # self.signal().progress.emit(100)
        # self.signal().done.emit(True)
        pass