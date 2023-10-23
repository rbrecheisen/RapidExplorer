from sqlalchemy.orm import Session

from rapidx.tests.data.file.filemodelfactory import FileModelFactory
from rapidx.tests.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.tests.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.tests.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory


class FileRegistrationHelper:
    # TODO: Make abstract class RegistrationHelper!
    def __init__(self, path: str, session: Session) -> None:
        self._path = path
        self._session = session

    def path(self) -> str:
        return self._path
    
    def session(self) -> Session:
        return self._session
    
    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModelFactory.create()
        fileSetModel = FileSetModelFactory.create(multiFileSetModel=multiFileSetModel)
        fileModel = FileModelFactory.create(fileSetModel=fileSetModel, path=self.path())
        # Save everything to SQL using a session
        self.session().add(multiFileSetModel)
        self.session().add(fileSetModel)
        self.session().add(fileModel)
        self.session().commit()
        return multiFileSetModel
