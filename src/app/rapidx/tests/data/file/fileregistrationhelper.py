from sqlalchemy.orm import Session

from rapidx.tests.data.registrationhelper import RegistrationHelper
from rapidx.tests.data.file.filemodelfactory import FileModelFactory
from rapidx.tests.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.tests.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.tests.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory


class FileRegistrationHelper(RegistrationHelper):
    def __init__(self, path: str, session: Session) -> None:
        super(FileRegistrationHelper, self).__init__(name=None, path=path, session=session)
    
    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModelFactory.create()
        fileSetModel = FileSetModelFactory.create(multiFileSetModel=multiFileSetModel)
        fileModel = FileModelFactory.create(fileSetModel=fileSetModel, path=self.path())
        self.session().add(multiFileSetModel)
        self.session().add(fileSetModel)
        self.session().add(fileModel)
        self.session().commit()
        return multiFileSetModel
