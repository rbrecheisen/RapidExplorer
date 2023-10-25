from sqlalchemy.orm import Session

from rapidx.tests.data.registrationhelper import RegistrationHelper
from rapidx.tests.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.tests.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.tests.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory


class FileSetRegistrationHelper(RegistrationHelper):
    def __init__(self, name: str, path: str, session: Session) -> None:
        super(FileSetRegistrationHelper, self).__init__(name=name, path=path, session=session)

    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModelFactory.create()
        fileSetModel = FileSetModelFactory.create(name=self.name(), path=self.path(), multiFileSetModel=multiFileSetModel)
        self.session().add(multiFileSetModel)
        self.session().add(fileSetModel)
        self.session().commit()
        return multiFileSetModel
