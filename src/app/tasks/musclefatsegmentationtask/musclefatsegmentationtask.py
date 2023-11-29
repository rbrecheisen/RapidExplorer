import os

from typing import List

from tasks.task import Task
from tasks.tasksignal import TaskSignal
from tasks.musclefatsegmentationtask.musclefatsegmentor import MuscleFatSegmentor
from data.fileset import FileSet


class MuscleFatSegmentationTask(Task):
    def __init__(self) -> None:
        super(MuscleFatSegmentationTask, self).__init__(name='MuscleFatSegmentationTask')
        self._inputFileSets = {}
        self._outputDirectory = None
        self._outputFilePaths = []
        self._signal = TaskSignal()
        self._nrSteps = 0

    def outputDirectory(self) -> str:
        # Move to Task class
        return self._outputDirectory

    def setOutputDirectory(self, outputDirectory: str) -> None:
        # Move to Task class
        self._outputDirectory = outputDirectory

    def outputFilePaths(self) -> List[str]:
        return self._outputFilePaths
    
    def signal(self) -> TaskSignal:
        return self._signal

    def addInputFileSet(self, fileSet: FileSet, name: str) -> None:
        # Move to Task class
        self._inputFileSets[name] = fileSet

    def getInputFileSet(self, name: str) -> FileSet:
        return self._inputFileSets[name]

    def run(self) -> List[str]:

        inputFilePaths = []
        for file in self._inputFileSets['dicomFiles'].files():
            inputFilePaths.append(file.path())
        tensorFlowModelFilePaths = []
        for file in self._inputFileSets['tensorFlowModelFiles'].files():
            tensorFlowModelFilePaths.append(file.path())
        
        os.makedirs(self.outputDirectory(), exist_ok=False)

        self._nrSteps = len(inputFilePaths) + len(tensorFlowModelFilePaths)
        
        segmentator = MuscleFatSegmentor()
        segmentator.signal().progress.connect(self.updateSegmentorProgress)
        segmentator.setInputFiles(inputFilePaths)
        segmentator.setModelFiles(tensorFlowModelFilePaths)
        segmentator.setOutputDirectory(self.outputDirectory())
        segmentator.setMode(MuscleFatSegmentor.ARGMAX)
        outputFilePaths = segmentator.execute()

        self._outputFilePaths = []
        for outputFilePath in outputFilePaths:
            self._outputFilePaths.append(outputFilePath)
        return self._outputFilePaths
    
    def updateSegmentorProgress(self, progress) -> None:
        progress = int((progress + 1) / self._nrSteps * 100)
        self.signal().progress.emit(progress)

    def segmentorFinished(self, value) -> None:
        self.signal().finished.emit(value)
