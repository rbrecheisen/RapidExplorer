import os

from typing import List

from tasks.task import Task
from tasks.tasksettingfilesetpath import TaskSettingFileSetPath
from tasks.tasksettingtext import TaskSettingText
from tasks.tasksettingfileset import TaskSettingFileSet
from tasks.musclefatsegmentationtask.musclefatsegmentor import MuscleFatSegmentor
from data.fileset import FileSet
from utils import createRandomName


class MuscleFatSegmentationTask(Task):
    def __init__(self) -> None:
        super(MuscleFatSegmentationTask, self).__init__(name='MuscleFatSegmentationTask')
        self.settings().add(
            TaskSettingFileSet(name='dicomFileSet', displayName='DICOM File Set'))
        self.settings().add(
            TaskSettingFileSet(name='tensorFlowModelFileSet', displayName='TensorFlow Model File Set'))
        self.settings().add(
            TaskSettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(
            TaskSettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self.settings().add(
            TaskSettingFileSet(name='outputFileSet', displayName='Output File Set', visible=False))

    def run(self) -> FileSet:
        # Collect input files
        inputFileSetName = self.settings().setting(name='dicomFileSet').value()
        inputFileSet = self._dataManager.fileSetByName(name=inputFileSetName)
        inputFilePaths = []
        for file in inputFileSet.files():
            inputFilePaths.append(file.path())
        # Collect tensorflow model files
        tensorFlowModelFileSetName = self.settings().setting(name='tensorFlowModelFileSet').value()
        tensorFlowModelFileSet = self._dataManager.fileSetByName(name=tensorFlowModelFileSetName)
        tensorFlowModelFilePaths = []
        for file in tensorFlowModelFileSet.files():
            tensorFlowModelFilePaths.append(file.path())
        # Collect other settings
        outputFileSetPath = self.settings().setting(name='outputFileSetPath').value()
        outputFileSetName = self.settings().setting(name='outputFileSetName').value()
        if not outputFileSetName:
            outputFileSetName = createRandomName(prefix='output')        
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        os.makedirs(outputFileSetPath, exist_ok=False)
        # Calculate number of steps required        
        self.setNrSteps(len(inputFilePaths) + len(tensorFlowModelFilePaths))
        # Run segmentation
        segmentator = MuscleFatSegmentor()
        segmentator.signal().progress.connect(self.updateSegmentorProgress)
        segmentator.setInputFiles(inputFilePaths)
        segmentator.setModelFiles(tensorFlowModelFilePaths)
        segmentator.setOutputDirectory(outputFileSetPath)
        segmentator.setMode(MuscleFatSegmentor.ARGMAX)
        segmentator.execute()
        # Build output file set
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetPath)
        outputFileSet.setName(outputFileSetName)
        self._dataManager.updateFileSet(fileSet=outputFileSet)
        self.settings().setting(name='outputFileSet').setValue(value=outputFileSet)
        return outputFileSet
    
    def updateSegmentorProgress(self, progress) -> None:
        progress = int((progress + 1) / self._nrSteps * 100)
        self.signal().progress.emit(progress)

    def segmentorFinished(self, value) -> None:
        self.signal().finished.emit(value)
