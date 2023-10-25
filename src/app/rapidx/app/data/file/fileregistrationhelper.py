from sqlalchemy.orm import Session

from rapidx.app.data.registrationhelper import RegistrationHelper
from rapidx.app.data.file.filemodelfactory import FileModelFactory
from rapidx.app.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory


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
