import os

from rapidx.app.plugins.viewplugin import ViewPlugin
from rapidx.app.plugins.taskplugin import TaskPlugin
from rapidx.app.plugins.pluginmanagerexception import PluginManagerException

PLUGINDIR = 'src/app/rapidx/plugins'


class PluginManager:
    def __init__(self) -> None:
        if not os.path.isdir(PLUGINDIR):
            raise PluginManagerException(f'Plugin directory {PLUGINDIR} not found')

    def loadAll(self):
        plugins = {}
        plugins = self.loadViewPlugins(PLUGINDIR, ViewPlugin, plugins)
        plugins = self.loadTaskPlugins(PLUGINDIR, TaskPlugin, plugins)
        return plugins

    def loadViewPlugins(self, pluginDirectory, baseClass, plugins):
        if not 'views' in plugins.keys():
            plugins['views'] = []
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
                            plugins[category].append(attribute)
        return plugins

    def loadTaskPlugins(self, pluginDirectory, baseClass, plugins):
        if not 'tasks' in plugins.keys():
            plugins['views'] = []
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
                            plugins[category].append(attribute)
        return plugins