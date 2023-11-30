import os

from typing import List

from tasks.task import Task
from tasks.tasksettingtext import TaskSettingText
from tasks.tasksettingfileset import TaskSettingFileSet
from tasks.musclefatsegmentationtask.musclefatsegmentor import MuscleFatSegmentor
from data.fileset import FileSet


class MuscleFatSegmentationTask(Task):
    def __init__(self) -> None:
        super(MuscleFatSegmentationTask, self).__init__(name='MuscleFatSegmentationTask')
        self.settings().add(
            TaskSettingFileSet(name='dicomFileSet', displayName='DICOM File Set', optional=False))
        self.settings().add(
            TaskSettingFileSet(name='tensorFlowModelFileSet', displayName='TensorFlow Model File Set', optional=False))
        self.settings().add(
            TaskSettingText(name='outputFileSetDirectory', displayName='Output File Set Directory', optional=True))
        self.settings().add(
            TaskSettingFileSet(name='outputFileSet', displayName='Output File Set', optional=False, visible=False))

    def run(self) -> FileSet:
        inputFilePaths = []
        for file in self.settings().setting(name='dicomFileSet').value().files():
            inputFilePaths.append(file.path())
        tensorFlowModelFilePaths = []
        for file in self.settings().setting(name='tensorFlowModelFileSet').value().files():
            tensorFlowModelFilePaths.append(file.path())
        outputFileSetDirectory = self.settings().setting(name='outputFileSetDirectory').value()
        os.makedirs(outputFileSetDirectory, exist_ok=False)
        self.setNrSteps(len(inputFilePaths) + len(tensorFlowModelFilePaths))
        segmentator = MuscleFatSegmentor()
        segmentator.signal().progress.connect(self.updateSegmentorProgress)
        segmentator.setInputFiles(inputFilePaths)
        segmentator.setModelFiles(tensorFlowModelFilePaths)
        segmentator.setOutputDirectory(outputFileSetDirectory)
        segmentator.setMode(MuscleFatSegmentor.ARGMAX)
        segmentator.execute()
        # TODO: Build output fileset (also create file set model in database!)
        # These output file paths already exist, so you can call dataManager.importFileSet(fileSetPath=outputFileSetDirectory)
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetDirectory)
        self.settings().setting(name='outputFileSet').setValue(value=outputFileSet)
        return outputFileSet
    
    def updateSegmentorProgress(self, progress) -> None:
        progress = int((progress + 1) / self._nrSteps * 100)
        self.signal().progress.emit(progress)

    def segmentorFinished(self, value) -> None:
        self.signal().finished.emit(value)
