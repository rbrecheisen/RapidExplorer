import os
import importlib.util

from PySide6.QtWidgets import QWidget

# https://chat.openai.com/c/cb4e0a73-1bd4-4edd-99e7-d49575c4c31c


class ViewerPluginInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def loadData(self, data):
        raise NotImplementedError('Not implemented')

    def name(self):
        raise NotImplementedError('Not implemented')
    

def discoverPlugins(pluginDirectory, baseClass):
    plugins = []
    for filename in os.listdir(pluginDirectory):
        if filename.endswith('.py') and not filename.startswith('__'):
            moduleName = filename[:-3]
            file_path = os.path.join(pluginDirectory, filename)
            spec = importlib.util.spec_from_file_location(moduleName, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for attributeName in dir(module):
                attribute = getattr(module, attributeName)
                if issubclass(attribute, baseClass) and attribute is not baseClass:
                    plugins.append(attribute)
    return plugins


def discoverAdvancedPlugins(pluginRootDirectory, baseClass):
    plugins = []
    for item in os.listdir(pluginRootDirectory):
        itemPath = os.path.join(pluginRootDirectory, item)
        if os.path.isdir(itemPath) and not item.startswith('__'):
            spec = importlib.util.spec_from_file_location(
                item, os.path.join(itemPath, '__init__.py')
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attributeName in dir(module):
                    attribute = getattr(module, attributeName)
                    if isinstance(attribute, type) and issubclass(attribute, baseClass) and attribute is not baseClass:
                        plugins.append(attribute)
    return plugins


def discoverAdvancedPluginCategories(pluginRootDirectory, baseClass):
    categoryDirectories = [d for d in os.listdir(pluginRootDirectory) 
                     if os.path.isdir(os.path.join(pluginRootDirectory, d))]
    plugins = {}

    for category in categoryDirectories:
        categoryDirectoryPath = os.path.join(pluginRootDirectory, category)
        plugins[category] = []
        
        for item in os.listdir(categoryDirectoryPath):
            itemPath = os.path.join(categoryDirectoryPath, item)
            
            if os.path.isdir(itemPath) and not item.startswith('__'):
                spec = importlib.util.spec_from_file_location(item, os.path.join(itemPath, '__init__.py'))
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for attributeName in dir(module):
                        attribute = getattr(module, attributeName)
                        if isinstance(attribute, type) and issubclass(attribute, baseClass) and attribute is not baseClass:
                            plugins[category].append(attribute)
    return plugins


pluginDirectory = '/path/to/your/plugins'
viewPlugins = discoverAdvancedPlugins(pluginDirectory, ViewerPluginInterface)

for pluginClass in viewPlugins:
    pluginInstance = pluginClass()
