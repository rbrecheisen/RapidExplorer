from typing import Dict

from singleton import singleton
from plugins.tasks.task import Task
from plugins.viewers.viewer import Viewer
from plugins.pluginsignal import PluginSignal
from plugins.tasks.l3autosegmentationtask.l3autosegmentationtask import L3AutoSegmentationTask
from plugins.viewers.dicomviewer.dicomviewer import DicomViewer


@singleton
class PluginManager:
    def __init__(self) -> None:
        self._plugins = {}
        self._currentPlugin = None
        self._currentTaskPlugin = None
        self._currentViewerPlugin = None
        self._signal = PluginSignal()

    def plugins(self):
        return self._plugins
    
    def taskPlugins(self) -> Dict:
        if 'tasks' in self.plugins().keys():
            return self.plugins()['tasks']
        return {}
    
    def taskPlugin(self, name):
        if name in self.taskPlugins().keys():
            return self.taskPlugins()[name]
        return None
    
    def viewerPlugins(self) -> Dict:
        if 'viewers' in self.plugins().keys():
            return self.plugins()['viewers']
        return {}
    
    def viewerPlugin(self, name):
        if name in self.viewerPlugins().keys():
            return self.viewerPlugins()[name]
        return None
    
    def currentPlugin(self):
        return self._currentPlugin
    
    def setCurrentPlugin(self, plugin):
        self._currentPlugin = plugin
        self.signal().pluginChanged.emit(self._currentPlugin)

    def currentTaskPlugin(self):
        return self._currentTaskPlugin
    
    def setCurrentTaskPlugin(self, plugin):
        if self.isTaskPlugin(plugin):
            self._currentTaskPlugin = plugin
            self.signal().taskPluginChanged.emit(self._currentTaskPlugin)

    def currentViewerPlugin(self):
        return self._currentViewerPlugin
    
    def setCurrentViewerPlugin(self, plugin):
        if self.isViewerPlugin(plugin):
            self._currentViewerPlugin = plugin
            self.signal().viewerPluginChanged.emit(self._currentViewerPlugin)
    
    def isTaskPlugin(self, plugin) -> bool:
        return isinstance(plugin, Task)
    
    def isViewerPlugin(self, plugin) -> bool:
        return isinstance(plugin, Viewer)

    def signal(self):
        return self._signal

    def loadAll(self):
        self._plugins = {}
        self.loadTaskPlugins()
        self.loadViewerPlugins()
        return self._plugins
    
    def loadTaskPlugins(self) -> None:
        if 'tasks' not in self._plugins.keys():
            self._plugins['tasks'] = {}
        # plugin1 = CopyFileSetTask()
        # self._plugins['tasks'][plugin1.name()] = plugin1
        plugin2 = L3AutoSegmentationTask()
        self._plugins['tasks'][plugin2.name()] = plugin2
        return self._plugins   
    
    def loadViewerPlugins(self) -> None:
        if 'viewers' not in self._plugins.keys():
            self._plugins['viewers'] = {}
        plugin1 = DicomViewer()
        self._plugins['viewers'][plugin1.name()] = plugin1
        return self._plugins