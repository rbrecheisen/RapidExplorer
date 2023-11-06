import os
import importlib

from typing import Dict

from rapidx.app.singleton import Singleton, singleton
from rapidx.app.plugins.taskplugin import TaskPlugin
from rapidx.app.plugins.viewplugin import ViewPlugin
from rapidx.app.plugins.pluginmanagerexception import PluginManagerException

PLUGINDIR = 'src/app/rapidx/plugins'


@singleton
class PluginManager:
    def __init__(self) -> None:
        if not os.path.isdir(PLUGINDIR):
            raise PluginManagerException(f'Plugin directory {PLUGINDIR} not found')
        self._plugins = {}

    def plugins(self):
        return self._plugins
    
    def taskPlugins(self) -> Dict:
        if 'tasks' in self.plugins().keys():
            return self.plugins()['tasks']
        return {}
    
    def viewPlugins(self) -> Dict:
        if 'views' in self.plugins().keys():
            return self.plugins()['views']
        return {}

    def loadAll(self):
        self._plugins = {}
        self.loadTaskPlugins(PLUGINDIR, TaskPlugin)
        self.loadViewPlugins(PLUGINDIR, ViewPlugin)
        return self._plugins

    def loadTaskPlugins(self, pluginDirectory, baseClass):
        if not 'tasks' in self._plugins.keys():
            self._plugins['tasks'] = []
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
                            self._plugins['tasks'].append(attribute())
        return self._plugins
    
    def loadViewPlugins(self, pluginDirectory, baseClass):
        if not 'views' in self._plugins.keys():
            self._plugins['views'] = []
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
                            self._plugins['views'].append(attribute())
        return self._plugins