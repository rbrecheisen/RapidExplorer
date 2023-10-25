from sqlalchemy.orm import Session

from rapidx.tests.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.tests.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory


class MultiFileSetRegistrationHelper:
    # TODO: Make abstract class RegistrationHelper!
    def __init__(self, name: str, path: str, session: Session) -> None:
        self._name = name
        self._path = path
        self._session = session

    def name(self) -> str:
        return self._name

    def path(self) -> str:
        return self._path
    
    def session(self) -> Session:
        return self._session
    
    def execute(self) -> MultiFileSetModel:
        multiFileSetModel = MultiFileSetModelFactory.create(name=self.name(), path=self.path())
        self.session().add(multiFileSetModel)
        self.session().commit()
        return multiFileSetModel
