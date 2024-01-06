import os

from typing import List

from PySide6.QtCore import QSettings

from singleton import singleton
from widgets.viewers.viewer import Viewer
from widgets.viewers.viewermanagersignal import ViewerManagerSignal
from utils import SettingsIniFile

# SETTINGSFILEPATH = os.environ.get('SETTINGSPATH', 'settings.ini')
SETTINGSFILEPATH = SettingsIniFile().path()


@singleton
class ViewerManager:
    def __init__(self) -> None:
        self._viewers = {}
        self._currentViewer = None
        self._signal = ViewerManagerSignal()
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)
        self.loadViewers()

    def signal(self) -> ViewerManagerSignal:
        return self._signal
    
    def settings(self) -> QSettings:
        return self._settings
    
    def viewer(self, name: str) -> Viewer:
        return self._viewers[name]
    
    def viewers(self) -> List[Viewer]:
        return self._viewers.values()
    
    def viewerNames(self) -> List[str]:
        return self._viewers.keys()
    
    def setCurrentViewer(self, viewer: Viewer) -> None:
        if viewer and viewer.name() not in self._viewers.keys():
            raise RuntimeError(f'Viewer {viewer.name()} was never registered')
        self._currentViewer = viewer
        self.signal().currentViewerChanged.emit(self._currentViewer)

    def currentViewer(self) -> Viewer:
        return self._currentViewer
    
    def updateViewerSettings(self) -> None:
        self._currentViewer.updateSettings()

    def loadViewers(self) -> None:
        from widgets.viewers.dicomviewer.dicomviewer import DicomViewer
        self._viewers = {
            DicomViewer.NAME: DicomViewer(),
        }
