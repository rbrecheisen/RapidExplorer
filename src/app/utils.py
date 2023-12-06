import os
import sys
import pendulum
import importlib
import numpy as np

from typing import Dict, Any

from singleton import singleton


def createNameWithTimestamp(prefix: str=''):
    tz = pendulum.local_timezone()
    timestamp = pendulum.now(tz).strftime('%Y%m%d%H%M%S%f')[:17]
    if prefix != '' and not prefix.endswith('-'):
        prefix = prefix + '-'
    name = f'{prefix}{timestamp}'
    return name


def getPixelsFromDicomObject(p, normalize=False):
    pixels = p.pixel_array
    if not normalize:
        return pixels
    if normalize is True:
        return p.RescaleSlope * pixels + p.RescaleIntercept
    if isinstance(normalize, int):
        return (pixels + np.min(pixels)) / (np.max(pixels) - np.min(pixels)) * normalize
    if isinstance(normalize, list):
        return (pixels + np.min(pixels)) / (np.max(pixels) - np.min(pixels)) * normalize[1] + normalize[0]
    return pixels


@singleton
class SettingsIniFile:
    def __init__(self) -> None:
        self._path = os.path.join(os.path.dirname(sys.executable), 'settings.ini')
        if not os.path.isfile(self._path):
            self._path = 'settings.ini'

    def path(self) -> str:
        return self._path
    

@singleton
class GitCommit:
    def __init__(self) -> None:
        commitIdFilePath = os.path.join(os.path.dirname(sys.executable), 'gitcommitid.txt')
        if not os.path.isfile(commitIdFilePath):
            commitIdFilePath = 'gitcommitid.txt'
        self._commitId = open(commitIdFilePath, 'r').readline().strip()

    def id(self) -> str:
        return self._commitId
    

class ModuleLoader:
    @staticmethod
    def loadModuleClasses(moduleDirectoryPath: str, moduleBaseClass: Any) -> Dict[str, Any]:
        classes = {}
        moduleDirectoryName = os.path.split(moduleDirectoryPath)[1]
        for root, dirs, files in os.walk(moduleDirectoryPath):
            for fileName in files:
                filePath = os.path.join(root, fileName)
                if fileName == '__init__.py':
                    taskModule = filePath.split(os.path.sep)[-2]
                    if taskModule != moduleDirectoryName:
                        spec = importlib.util.spec_from_file_location(taskModule, filePath)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            for attributeName in dir(module):
                                attribute = getattr(module, attributeName)
                                if isinstance(attribute, type) and issubclass(attribute, moduleBaseClass) and attribute is not moduleBaseClass:
                                    classes[attribute.NAME] = attribute
                                    print(f'Loaded module {attribute.NAME}')
        return classes