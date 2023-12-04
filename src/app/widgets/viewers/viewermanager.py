import os

from typing import List

from PySide6.QtCore import QSettings, QThreadPool

from singleton import singleton
from widgets.viewers.viewer import Viewer
from widgets.viewers.viewermanagersignal import ViewerManagerSignal
from settings.settings import Settings

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
    
    def viewerSettings(self, name: str) -> Settings:
        return self._viewerSettings[name]
    
    def updateViewerSettings(self, name: str, viewerSettings: Settings) -> None:
        self._viewerSettings[name] = viewerSettings

    def currentViewerSettings(self) -> Settings:
        return self._viewerSettings[self.currentViewerDefinitionName()]

    def loadViewerDefinitionsAndSettings(self) -> None:
        from widgets.viewers.dicomviewer.dicomviewer import DicomViewer
        self._viewerDefinitions = {
            DicomViewer.NAME: DicomViewer,
        }
        self._viewerSettings = {}
        for viewerDefinitionName in self._viewerDefinitions.keys():
            viewerDefinition = self._viewerDefinitions[viewerDefinitionName]
            viewer = viewerDefinition()
            viewerSettings = viewer.settings()
            self._viewerSettings[viewerDefinitionName] = viewerSettings

    def createViewer(self, name: str) -> Viewer:
        viewerDefinition = self._viewerDefinitions[name]
        viewer = viewerDefinition()
        return viewer
