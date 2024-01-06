from PySide6.QtWidgets import QWidget

from settings.settings import Settings


class Viewer(QWidget):
    NAME = None
    
    def __init__(self) -> None:
        super(Viewer, self).__init__()
        self._settings = Settings(name=self.NAME)

    def name(self) -> str:
        return self.NAME
    
    def settings(self) -> Settings:
        return self._settings
    
    def setSettings(self, settings: Settings) -> None:
        self._settings = settings

    def updateSettings(self) -> None:
        raise NotImplementedError('Not implemented')