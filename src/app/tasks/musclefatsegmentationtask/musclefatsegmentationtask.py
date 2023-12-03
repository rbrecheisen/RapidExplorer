import os

from typing import List

from tasks.task import Task
from tasks.tasksignal import TaskSignal
from tasks.tasksettingfilesetpath import TaskSettingFileSetPath
from tasks.tasksettingtext import TaskSettingText
from tasks.tasksettingfileset import TaskSettingFileSet
from tasks.musclefatsegmentationtask.musclefatsegmentor import MuscleFatSegmentor
from data.fileset import FileSet
from utils import createNameWithTimestamp


class MuscleFatSegmentationTask(Task):
    NAME = 'MuscleFatSegmentationTask'
    
    def __init__(self) -> None:
        super(MuscleFatSegmentationTask, self).__init__(name='MuscleFatSegmentationTask')
        self.settings().add(TaskSettingFileSet(name='dicomFileSetName', displayName='DICOM File Set'))
        self.settings().add(TaskSettingFileSet(name='tensorFlowModelFileSetName', displayName='TensorFlow Model File Set'))
        self.settings().add(TaskSettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(TaskSettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        # Collect input files
        inputFileSetName = self.settings().setting(name='dicomFileSetName').value()
        inputFileSet = self._dataManager.fileSetByName(name=inputFileSetName)
        inputFilePaths = []
        for file in inputFileSet.files():
            inputFilePaths.append(file.path())
        # Collect tensorflow model files
        tensorFlowModelFileSetName = self.settings().setting(name='tensorFlowModelFileSetName').value()
        tensorFlowModelFileSet = self._dataManager.fileSetByName(name=tensorFlowModelFileSetName)
        tensorFlowModelFilePaths = []
        for file in tensorFlowModelFileSet.files():
            tensorFlowModelFilePaths.append(file.path())
        # Collect other settings
        outputFileSetPath = self.settings().setting(name='outputFileSetPath').value()
        outputFileSetName = self.settings().setting(name='outputFileSetName').value()
        if not outputFileSetName:
            outputFileSetName = createNameWithTimestamp(prefix='output')        
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        os.makedirs(outputFileSetPath, exist_ok=False)
        # Calculate number of steps required        
        self.setNrSteps(len(inputFilePaths) + len(tensorFlowModelFilePaths))
        # Run segmentation
        segmentor = MuscleFatSegmentor(parentTask=self)
        segmentor.setInputFiles(inputFilePaths)
        segmentor.setModelFiles(tensorFlowModelFilePaths)
        segmentor.setOutputDirectory(outputFileSetPath)
        segmentor.setMode(MuscleFatSegmentor.ARGMAX)
        segmentor.execute()
        # Build output file set
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetPath)
        outputFileSet.setName(outputFileSetName)
        outputFileSet = self._dataManager.updateFileSet(fileSet=outputFileSet)
        self.signal().finished.emit(outputFileSet)
        return outputFileSet
    
    def segmentorProgress(self, progress) -> None:
        progress = int((progress + 1) / (self._nrSteps + 1) * 100)
        self.signal().progress.emit(progress)