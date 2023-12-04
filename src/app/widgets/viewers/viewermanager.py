import os

from typing import List

from PySide6.QtCore import QSettings, QThreadPool

from singleton import singleton
from widgets.viewers.viewermanagersignal import ViewerManagerSignal

SETTINGSFILEPATH = os.environ.get('SETTINGSPATH', 'settings.ini')


@singleton
class ViewerManager:
    def __init__(self) -> None:
        self._viewerDefinitions = {}
        self._viewerSettings = {}
        self._signal = ViewerManagerSignal()
        self._settings = QSettings(SETTINGSFILEPATH, QSettings.Format.IniFormat)
        self._currentViewerDefinitionName = None
        self._currentViewerSettings = None
        self.loadViewerDefinitionsAndSettings()

    def viewerDefinitions(self) -> List[Viewer]:
        return self._viewerDefinitions.values()
    
    def viewerDefinitionNames(self) -> List[str]:
        return self._viewerDefinitions.keys()
    
    def signal(self) -> ViewerManagerSignal:
        return self._signal
    
    def settings(self) -> QSettings:
        return self._settings
    
    def viewerDefinition(self, name: str) -> Viewer:
        return self._viewerDefinitions[name]
    
    def currentViewerDefinitionName(self) -> str:
        return self._currentViewerDefinitionName
    
    def setCurrentViewerDefinitionName(self, currentViewerDefinitionName: str) -> None:
        if currentViewerDefinitionName not in self._viewerDefinitions.keys():
            raise RuntimeError(f'Class definition for viewer {currentViewerDefinitionName} does not exist')
        self._currentViewerDefinitionName = currentViewerDefinitionName

    def nrViewerDefinitions(self) -> int:
        return len(self._viewerDefinitions.keys())
    
    def viewerSettings(self, name: str) -> ViewerSettings:
        return self._viewerSettings[name]
    
    def updateViewerSettings(self, name: str, viewerSettings: ViewerSettings) -> None:
        self._viewerSettings[name] = viewerSettings

    def currentViewerSettings(self) -> ViewerSettings:
        return self._viewerSettings[self.currentViewerDefinitionName()]

    def loadViewerDefinitionsAndSettings(self) -> None:
        pass

    def createViewer(self, name: str) -> Viewer:
        viewerDefinition = self._viewerDefinitions[name]
        viewer = viewerDefinition()
        return viewer
