from sqlalchemy.orm import Session


class RegistrationHelper:
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