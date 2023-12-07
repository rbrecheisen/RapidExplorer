import os
import sys
import math
import pendulum
import importlib
import pydicom
import numpy as np

from typing import Dict, Any, List

from singleton import singleton


def createNameWithTimestamp(prefix: str='') -> str:
    tz = pendulum.local_timezone()
    timestamp = pendulum.now(tz).strftime('%Y%m%d%H%M%S%f')[:17]
    if prefix != '' and not prefix.endswith('-'):
        prefix = prefix + '-'
    name = f'{prefix}{timestamp}'
    return name


def currentTimeInMilliseconds() -> int:
    return int(round(time.time() * 1000))


def currentTimeInSeconds() -> int:
    return int(round(currentTimeInMilliseconds() / 1000.0))


def elapsedMilliseconds(startTimeInMilliseconds: int) -> int:
    return currentTimeInMilliseconds() - startTimeInMilliseconds


def elapsedSeconds(startTimeInSeconds: int) -> int:
    return currentTimeInSeconds() - startTimeInSeconds


def duration(seconds: int) -> str:
    h = int(math.floor(seconds/3600.0))
    remainder = seconds - h * 3600
    m = int(math.floor(remainder/60.0))
    remainder = remainder - m * 60
    s = int(math.floor(remainder))
    return '{} hours, {} minutes, {} seconds'.format(h, m, s)


def getPixelsFromDicomObject(p: pydicom.FileDataset, normalize: bool=False) -> np.array:
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


def convertLabelsTo157(labelImage: np.array) -> np.array:
    labelImage157 = np.copy(labelImage)
    labelImage157[labelImage157 == 1] = 1
    labelImage157[labelImage157 == 2] = 5
    labelImage157[labelImage157 == 3] = 7
    return labelImage157


def normalizeBetween(img: np.array, minBound: int, maxBound: int) -> np.array:
    img = (img - minBound) / (maxBound - minBound)
    img[img > 1] = 0
    img[img < 0] = 0
    c = (img - np.min(img))
    d = (np.max(img) - np.min(img))
    img = np.divide(c, d, np.zeros_like(c), where=d != 0)
    return img


def applyWindowCenterAndWidth(image: np.array, center: int, width: int) -> np.array:
    imageMin = center - width // 2
    imageMax = center + width // 2
    windowedImage = np.clip(image, imageMin, imageMax)
    windowedImage = ((windowedImage - imageMin) / (imageMax - imageMin)) * 255.0
    return windowedImage.astype(np.uint8)


def albertaColorMap() -> List[List[int]]:
    colorMap = []
    for i in range(256):
        if i == 1:  # muscle
            colorMap.append([255, 0, 0])
        elif i == 2:  # inter-muscular adipose tissue
            colorMap.append([0, 255, 0])
        elif i == 5:  # visceral adipose tissue
            colorMap.append([255, 255, 0])
        elif i == 7:  # subcutaneous adipose tissue
            colorMap.append([0, 255, 255])
        elif i == 12:  # unknown
            colorMap.append([0, 0, 255])
        else:
            colorMap.append([0, 0, 0])
    return colorMap


def applyColorMap(pixels: np.array, color_map: List[List[int]]) -> np.array:
    pixelsNew = np.zeros((*pixels.shape, 3), dtype=np.uint8)
    np.take(color_map, pixels, axis=0, out=pixelsNew)
    return pixelsNew


def tagPixels(tagFilePath: str) -> np.array:
    f = open(tagFilePath, 'rb')
    f.seek(0)
    byte = f.read(1)
    # Make sure to check the byte-value in Python 3!!
    while byte != b'':
        byteHex = binascii.hexlify(byte)
        if byteHex == b'0c':
            break
        byte = f.read(1)
    values = []
    f.read(1)
    while byte != b'':
        v = struct.unpack('b', byte)
        values.append(v)
        byte = f.read(1)
    values = np.asarray(values)
    values = values.astype(np.uint16)
    return values


def calculateArea(labels, label, pixelSpacing):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    area = np.sum(mask) * (pixelSpacing[0] * pixelSpacing[1]) / 100.0
    return area

def calculateMeanRadiationAttennuation(image, labels, label):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    subtracted = image * mask
    maskSum = np.sum(mask)
    if maskSum > 0.0:
        meanRadiationAttenuation = np.sum(subtracted) / np.sum(mask)
    else:
        print('Sum of mask pixels is zero, return zero radiation attenuation')
        meanRadiationAttenuation = 0.0
    return meanRadiationAttenuation


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