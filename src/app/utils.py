import os
import sys
import pendulum
import numpy as np

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
        self._path = 'settings.ini'
        if not os.path.isfile(self._path):
            self._path = os.path.join(os.path.dirname(sys.executable), 'settings.ini')

    def path(self) -> str:
        return self._path
    

@singleton
class GitCommit:
    def __init__(self) -> None:
        commitIdFilePath = 'gitcommitid.txt'
        if not os.path.isfile(commitIdFilePath):
            commitIdFilePath = os.path.join(os.path.dirname(sys.executable), 'gitcommitid.txt')
        self._commitId = open(commitIdFilePath, 'r').readline().strip()

    def id(self) -> str:
        return self._commitId