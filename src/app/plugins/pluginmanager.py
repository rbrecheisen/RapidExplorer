import os
import pkgutil
import importlib

from typing import Dict

from singleton import singleton
from plugins.tasks.task import Task
from plugins.viewers.viewer import Viewer
from plugins.pluginsignal import PluginSignal
from plugins.tasks.copyfilesettask.copyfilesettask import CopyFileSetTask
from plugins.viewers.dicomviewer.dicomviewer import DicomViewer


@singleton
class PluginManager:
    def __init__(self) -> None:
        # if not os.path.isdir(PLUGINDIR):
        #     raise PluginManagerException(f'Plugin directory {PLUGINDIR} not found')
        self._plugins = {}
        self._currentPlugin = None
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
    
    def viewPlugins(self) -> Dict:
        if 'viewers' in self.plugins().keys():
            return self.plugins()['viewers']
        return {}
    
    def viewPlugin(self, name):
        if name in self.viewPlugins().keys():
            return self.viewPlugins()[name]
        return None
    
    def currentPlugin(self):
        return self._currentPlugin
    
    def isTaskPlugin(self, plugin) -> bool:
        return isinstance(plugin, Task)
    
    def isViewPlugin(self, plugin) -> bool:
        return isinstance(plugin, Viewer)

    def signal(self):
        return self._signal

    def setCurrentPlugin(self, plugin):
        self._currentPlugin = plugin
        self.signal().pluginChanged.emit(self._currentPlugin)

    def loadAll(self):
        self._plugins = {}
        # self.loadTaskPlugins(PLUGINDIR, Task)
        self.loadTaskPlugins()
        # self.loadViewerPlugins(PLUGINDIR, Viewer)
        self.loadViewerPlugins()
        return self._plugins
    
    def loadTaskPlugins(self) -> None:
        if 'tasks' not in self._plugins.keys():
            self._plugins['tasks'] = {}
        plugin1 = CopyFileSetTask()
        self._plugins['tasks'][plugin1.name()] = plugin1     
        return self._plugins   
    
    # def loadTaskPlugins(self, pluginDirectory, baseClass):
    #     if 'tasks' not in self._plugins.keys():
    #         self._plugins['tasks'] = {}
    #     taskPluginDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks')
    #     # Iterate over all modules in the specified directory
    #     for finder, name, ispkg in pkgutil.iter_modules([taskPluginDirectory]):
    #         # Skip if it's a package
    #         if ispkg:
    #             continue
    #         # Load the module
    #         pluginModulePath = os.path.join(taskPluginDirectory, name)
    #         spec = importlib.util.spec_from_file_location(name, os.path.join(pluginModulePath, '__init__.py'))
    #         if spec and spec.loader:
    #             module = importlib.util.module_from_spec(spec)
    #             spec.loader.exec_module(module)
    #             # Iterate over attributes in the module and check for subclasses of baseClass
    #             for attributeName in dir(module):
    #                 attribute = getattr(module, attributeName)
    #                 if isinstance(attribute, type) and issubclass(attribute, baseClass) and attribute is not baseClass:
    #                     plugin = attribute()
    #                     self._plugins['tasks'][plugin.name()] = plugin
    #     return self._plugins

    # def loadTaskPlugins(self, pluginDirectory, baseClass):
    #     if not 'tasks' in self._plugins.keys():
    #         self._plugins['tasks'] = {}
    #     # taskPluginDirectory = os.path.join(pluginDirectory, 'tasks')
    #     taskPluginDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks')
    #     for pluginModule in os.listdir(taskPluginDirectory):
    #         pluginModulePath = os.path.join(taskPluginDirectory, pluginModule)
    #         if os.path.isdir(pluginModulePath) and not pluginModule.startswith('__'):
    #             spec = importlib.util.spec_from_file_location(pluginModule, os.path.join(pluginModulePath, '__init__.py'))
    #             if spec and spec.loader:
    #                 module = importlib.util.module_from_spec(spec)
    #                 spec.loader.exec_module(module)
    #                 for attributeName in dir(module):
    #                     attribute = getattr(module, attributeName)
    #                     if isinstance(attribute, type) and issubclass(attribute, baseClass) and attribute is not baseClass:
    #                         plugin = attribute()
    #                         self._plugins['tasks'][plugin.name()] = plugin
    #     return self._plugins

    def loadViewerPlugins(self) -> None:
        if 'viewers' not in self._plugins.keys():
            self._plugins['viewers'] = {}
        plugin1 = DicomViewer()
        self._plugins['viewers'][plugin1.name()] = plugin1
        return self._plugins
    
    # def loadViewerPlugins(self, pluginDirectory, baseClass):
    #     if 'viewers' not in self._plugins.keys():
    #         self._plugins['viewers'] = {}
    #     viewerPluginDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viewers')
    #     # Iterate over all modules in the specified directory
    #     for finder, name, ispkg in pkgutil.iter_modules([viewerPluginDirectory]):
    #         # Skip if it's a package
    #         if ispkg:
    #             continue
    #         # Load the module
    #         pluginModulePath = os.path.join(viewerPluginDirectory, name)
    #         spec = importlib.util.spec_from_file_location(name, os.path.join(pluginModulePath, '__init__.py'))
    #         if spec and spec.loader:
    #             module = importlib.util.module_from_spec(spec)
    #             spec.loader.exec_module(module)
    #             # Iterate over attributes in the module and check for subclasses of baseClass
    #             for attributeName in dir(module):
    #                 attribute = getattr(module, attributeName)
    #                 if isinstance(attribute, type) and issubclass(attribute, baseClass) and attribute is not baseClass:
    #                     plugin = attribute()
    #                     self._plugins['viewers'][plugin.name()] = plugin
    #     return self._plugins

    # def loadViewPlugins(self, pluginDirectory, baseClass):
    #     if not 'viewers' in self._plugins.keys():
    #         self._plugins['viewers'] = {}
    #     viewPluginDirectory = os.path.join(pluginDirectory, 'viewers')
    #     for pluginModule in os.listdir(viewPluginDirectory):
    #         pluginModulePath = os.path.join(viewPluginDirectory, pluginModule)
    #         if os.path.isdir(pluginModulePath) and not pluginModule.startswith('__'):
    #             spec = importlib.util.spec_from_file_location(pluginModule, os.path.join(pluginModulePath, '__init__.py'))
    #             if spec and spec.loader:
    #                 module = importlib.util.module_from_spec(spec)
    #                 spec.loader.exec_module(module)
    #                 for attributeName in dir(module):
    #                     attribute = getattr(module, attributeName)
    #                     if isinstance(attribute, type) and issubclass(attribute, baseClass) and attribute is not baseClass:
    #                         plugin = attribute()
    #                         self._plugins['viewers'][plugin.name()] = plugin
    #     return self._plugins