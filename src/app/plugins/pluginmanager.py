import os
import importlib

from typing import Dict

from singleton import singleton
from plugins.taskplugin import TaskPlugin
from plugins.viewplugin import ViewPlugin
from plugins.pluginsignal import PluginSignal
from plugins.pluginmanagerexception import PluginManagerException

PLUGINDIR = 'src/experiments/backgroundloading/example2/plugins/plugins'


@singleton
class PluginManager:
    def __init__(self) -> None:
        if not os.path.isdir(PLUGINDIR):
            raise PluginManagerException(f'Plugin directory {PLUGINDIR} not found')
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
        if 'views' in self.plugins().keys():
            return self.plugins()['views']
        return {}
    
    def viewPlugin(self, name):
        if name in self.viewPlugins().keys():
            return self.viewPlugins()[name]
        return None
    
    def currentPlugin(self):
        return self._currentPlugin

    def signal(self):
        return self._signal

    def setCurrentPlugin(self, plugin):
        # This method is called by other components in RapidExplorer
        # For example, the views dock widget has a menu where the user
        # can select a view plugin
        self._currentPlugin = plugin
        self.signal().pluginChanged.emit(self._currentPlugin)

    def loadAll(self):
        self._plugins = {}
        self.loadTaskPlugins(PLUGINDIR, TaskPlugin)
        self.loadViewPlugins(PLUGINDIR, ViewPlugin)
        return self._plugins

    def loadTaskPlugins(self, pluginDirectory, baseClass):
        if not 'tasks' in self._plugins.keys():
            self._plugins['tasks'] = {}
        taskPluginDirectory = os.path.join(pluginDirectory, 'tasks')
        for pluginModule in os.listdir(taskPluginDirectory):
            pluginModulePath = os.path.join(taskPluginDirectory, pluginModule)
            if os.path.isdir(pluginModulePath) and not pluginModule.startswith('__'):
                spec = importlib.util.spec_from_file_location(pluginModule, os.path.join(pluginModulePath, '__init__.py'))
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for attributeName in dir(module):
                        attribute = getattr(module, attributeName)
                        if isinstance(attribute, type) and issubclass(attribute, baseClass) and attribute is not baseClass:
                            plugin = attribute()
                            self._plugins['tasks'][plugin.name()] = plugin
        return self._plugins
    
    def loadViewPlugins(self, pluginDirectory, baseClass):
        if not 'views' in self._plugins.keys():
            self._plugins['views'] = {}
        viewPluginDirectory = os.path.join(pluginDirectory, 'views')
        for pluginModule in os.listdir(viewPluginDirectory):
            pluginModulePath = os.path.join(viewPluginDirectory, pluginModule)
            if os.path.isdir(pluginModulePath) and not pluginModule.startswith('__'):
                spec = importlib.util.spec_from_file_location(pluginModule, os.path.join(pluginModulePath, '__init__.py'))
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for attributeName in dir(module):
                        attribute = getattr(module, attributeName)
                        if isinstance(attribute, type) and issubclass(attribute, baseClass) and attribute is not baseClass:
                            plugin = attribute()
                            self._plugins['views'][plugin.name()] = plugin
        return self._plugins