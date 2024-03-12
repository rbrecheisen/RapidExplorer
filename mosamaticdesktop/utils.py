import os
import time
import sys
import math
import pickle
import pendulum
import importlib
import pydicom
import binascii
import struct
import pydicom.errors
import numpy as np
# import matplotlib
# matplotlib.use('Qt5Agg')
# import matplotlib.pyplot as plt

from PIL import Image
from typing import Dict, Any, List

from PySide6.QtGui import QImage
from PySide6.QtCore import QSettings

from mosamaticdesktop.singleton import singleton
from mosamaticdesktop.operatingsystem import OperatingSystem
from mosamaticdesktop.data.file import File
from mosamaticdesktop.data.filecontent import FileContent
from mosamaticdesktop.data.filecontentcache import FileContentCache


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


def readFromCache(file: File) -> FileContent:
    cache = FileContentCache()
    return cache.get(id=file.id())

def writeToCache(file: File, fileObject: Any) -> None:
    content = FileContent(file=file, fileObject=fileObject)
    cache = FileContentCache()
    cache.add(content)
    # Return content rightaway for continued processing
    # after updating cache
    return content


def isDicomFile(filePath: str) -> bool:
    try:
        pydicom.dcmread(filePath, stop_before_pixels=True)
        return True
    except pydicom.errors.InvalidDicomError:
        return False
    

def isNumPyFile(filePath: str) -> bool:
    return filePath.endswith('.npy')
    

def isTagFile(filePath: str) -> bool:
    return filePath.endswith('.tag')


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


class ColorMap:
    def __init__(self, name: str) -> None:
        self._name = name
        self._values = []

    def name(self) -> str:
        return self._name
    
    def values(self) -> List[List[int]]:
        return self._values
    

class GrayScaleColorMap(ColorMap):
    def __init__(self) -> None:
        super(GrayScaleColorMap, self).__init__(name='GrayScaleColorMap')
        # Implement your own gray scale map or let NumPy do this more efficiently?
        pass    

class AlbertaColorMap(ColorMap):
    def __init__(self) -> None:
        super(AlbertaColorMap, self).__init__(name='AlbertaColorMap')
        for i in range(256):
            if i == 1:  # muscle
                self.values().append([255, 0, 0])
            elif i == 2:  # inter-muscular adipose tissue
                self.values().append([0, 255, 0])
            elif i == 5:  # visceral adipose tissue
                self.values().append([255, 255, 0])
            elif i == 7:  # subcutaneous adipose tissue
                self.values().append([0, 255, 255])
            elif i == 12:  # unknown
                self.values().append([0, 0, 255])
            else:
                self.values().append([0, 0, 0])


def applyColorMap(pixels: np.array, colorMap: ColorMap) -> np.array:
    pixelsNew = np.zeros((*pixels.shape, 3), dtype=np.uint8)
    np.take(colorMap.values(), pixels, axis=0, out=pixelsNew)
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


def loadNumPyArray(filePath: str) -> np.array:
    return np.load(filePath)


def convertDicomToNumPyArray(dicomFilePath: str, windowLevel: int=50, windowWidth: int=400, normalize=True) -> np.array:
    p = pydicom.dcmread(dicomFilePath)
    pixels = p.pixel_array
    pixels = pixels.reshape(p.Rows, p.Columns)
    if normalize:
        b = p.RescaleIntercept
        m = p.RescaleSlope
        pixels = m * pixels + b
    pixels = applyWindowCenterAndWidth(pixels, windowLevel, windowWidth)
    return pixels


def convertNumPyArrayToPngImage(
        numpyArrayFilePathOrObject: str, outputDirectoryPath: str, colorMap: ColorMap=None, pngImageFileName: str=None, figureWidth: int=10, figureHeight: int=10) -> str:
    if isinstance(numpyArrayFilePathOrObject, str):
        numpyArray = loadNumPyArray(numpyArrayFilePathOrObject)
    else:
        numpyArray = numpyArrayFilePathOrObject
        if not pngImageFileName:
            raise RuntimeError('PNG file name required for NumPy array object')
    if colorMap:
        numpyArray = applyColorMap(pixels=numpyArray, colorMap=colorMap)
    image = Image.fromarray(numpyArray)
    # fig = plt.figure(figsize=(figureWidth, figureHeight))
    # ax = fig.add_subplot(1, 1, 1)
    # if colorMap:
    #     plt.imshow(numpyArray)
    # else:
    #     plt.imshow(numpyArray, cmap='gray')
    # ax.axis('off')
    if not pngImageFileName:
        numpyArrayFileName = os.path.split(numpyArrayFilePathOrObject)[1]
        pngImageFileName = numpyArrayFileName + '.png'      
    elif not pngImageFileName.endswith('.png'):
        pngImageFileName += '.png'
    pngImageFilePath = os.path.join(outputDirectoryPath, pngImageFileName)
    # plt.savefig(pngImageFilePath, bbox_inches='tight')
    # plt.close('all')
    image.save(pngImageFilePath)
    return pngImageFilePath


def convertNumPyArrayToRgbQImage(numpyArray: np.array, colorMap: ColorMap) -> QImage:
    numpyArray = applyColorMap(pixels=numpyArray, colorMap=colorMap)
    h, w, _ = numpyArray.shape
    image = QImage(numpyArray.data.tobytes(), w, h, QImage.Format_RGB888)
    return image


def calculateArea(labels, label, pixelSpacing):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    area = np.sum(mask) * (pixelSpacing[0] * pixelSpacing[1]) / 100.0
    return area


def calculateIndex(area: float, height: float):
    return area / (height * height)


def calculateMeanRadiationAttennuation(image, labels, label):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    subtracted = image * mask
    maskSum = np.sum(mask)
    if maskSum > 0.0:
        meanRadiationAttenuation = np.sum(subtracted) / np.sum(mask)
    else:
        # print('Sum of mask pixels is zero, return zero radiation attenuation')
        meanRadiationAttenuation = 0.0
    return meanRadiationAttenuation


def calculateDiceScore(groundTruth, prediction, label):
    numerator = prediction[groundTruth == label]
    numerator[numerator != label] = 0
    n = groundTruth[prediction == label]
    n[n != label] = 0
    if np.sum(numerator) != np.sum(n):
        raise RuntimeError('Mismatch in Dice score calculation!')
    denominator = (np.sum(prediction[prediction == label]) + np.sum(groundTruth[groundTruth == label]))
    diceScore = np.sum(numerator) * 2.0 / denominator
    return diceScore


@singleton
class GitCommit:
    def __init__(self) -> None:
        commitIdFilePath = os.path.join(os.path.dirname(sys.executable), 'gitcommitid.txt')
        if not os.path.isfile(commitIdFilePath):
            commitIdFilePath = 'gitcommitid.txt'
        self._commitId = open(commitIdFilePath, 'r').readline().strip()

    def id(self) -> str:
        return self._commitId
    

@singleton
class Configuration:
    def __init__(self) -> None:
        self._configDirectory = os.path.join(OperatingSystem.homeDirectory(), '.mosamatic')

    def configDirectory(self) -> str:
        return self._configDirectory
    
    def taskConfigDirectory(self, taskName: str) -> str:
        taskConfigDirectory = os.path.join(self._configDirectory, taskName)
        if not os.path.isdir(taskConfigDirectory):
            os.makedirs(taskConfigDirectory, exist_ok=False)
        return taskConfigDirectory
    
    def taskConfigSubDirectory(self, taskName: str, dirName: str) -> str:
        taskConfigDirectory = self.taskConfigDirectory(taskName=taskName)
        taskConfigSubDirectory = os.path.join(taskConfigDirectory, dirName)
        if not os.path.isdir(taskConfigSubDirectory):
            os.makedirs(taskConfigSubDirectory, exist_ok=False)
        return taskConfigSubDirectory
    
    def qSettings(self) -> QSettings:
        settingsPath = os.path.join(self.configDirectory(), 'settings.ini')
        return QSettings(settingsPath, QSettings.Format.IniFormat)
    

class ModuleLoader:
    @staticmethod
    def loadModuleClasses(moduleDirectoryPath: str, moduleBaseClass: Any, fileNameEndsWith: str) -> Dict[str, Any]:
        classes = {}
        moduleDirectoryName = os.path.split(moduleDirectoryPath)[1]
        for root, dirs, files in os.walk(moduleDirectoryPath):
            for fileName in files:
                filePath = os.path.join(root, fileName)
                if fileName.endswith(fileNameEndsWith):
                    taskModule = filePath.split(os.path.sep)[-2]
                    if taskModule != moduleDirectoryName:
                        spec = importlib.util.spec_from_file_location(taskModule, filePath)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            for attributeName in dir(module):
                                attribute = getattr(module, attributeName)
                                if isinstance(attribute, type) and issubclass(attribute, moduleBaseClass) and attribute is not moduleBaseClass:
                                    classes[attribute.NAME()] = attribute
        return classes
    

class ParameterLoader:
    @staticmethod
    def loadParameterClasses(parameterDirectoryPath: str, parameterBaseClass: Any) -> Dict[str, Any]:
        classes = {}
        parameterDirectoryName = os.path.split(parameterDirectoryPath)[1]
        for root, dirs, files in os.walk(parameterDirectoryPath):
            for fileName in files:
                filePath = os.path.join(root, fileName)
                if fileName.endswith('parameter.py'):
                    taskModule = filePath.split(os.path.sep)[-1]
                    if taskModule != parameterDirectoryName:
                        taskModule = f'tasks.{taskModule[:-3]}'
                        spec = importlib.util.spec_from_file_location(taskModule, filePath)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            for attributeName in dir(module):
                                attribute = getattr(module, attributeName)
                                if isinstance(attribute, type) and issubclass(attribute, parameterBaseClass) and attribute is not parameterBaseClass:
                                    classes[attribute.NAME()] = attribute
        return classes
