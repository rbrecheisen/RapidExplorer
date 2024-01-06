import os
import shutil

from typing import List

from tasks.task import Task
from tasks.taskoutput import TaskOutput
from tasks.tasksignal import TaskSignal
from settings.settingfilesetpath import SettingFileSetPath
from settings.settingtext import SettingText
from settings.settingfileset import SettingFileSet
from settings.settinglabel import SettingLabel
from settings.settingboolean import SettingBoolean
from tasks.musclefatsegmentationtask.musclefatsegmentor import MuscleFatSegmentor
from data.fileset import FileSet
from utils import createNameWithTimestamp

DESCRIPTION = """
This task creates muscle and fat segmentation masks for the given DICOM file set using the selected TensorFlow model.
"""


class MuscleFatSegmentationTask(Task):
    NAME = 'MuscleFatSegmentationTask'
    
    def __init__(self) -> None:
        super(MuscleFatSegmentationTask, self).__init__()
        self.settings().add(SettingLabel(name='description', value=DESCRIPTION))
        self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='DICOM File Set'))
        self.settings().add(SettingFileSet(name='tensorFlowModelFileSetName', displayName='TensorFlow Model File Set'))
        self.settings().add(SettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(SettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self.settings().add(SettingBoolean(name='overwritePreviousOutputFileSet', displayName='Overwrite Previous Output File Set', defaultValue=True))
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
        overwritePreviousOutputFileSet = self.settings().setting(name='overwritePreviousOutputFileSet').value()
        os.makedirs(outputFileSetPath, exist_ok=overwritePreviousOutputFileSet)
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
        taskOutput = TaskOutput(fileSet=outputFileSet, errorInfo=[])
        self.signal().finished.emit(taskOutput)
        return taskOutput
    
    def segmentorProgress(self, progress) -> None:
        progress = int((progress + 1) / (self._nrSteps + 1) * 100)
        self.signal().progress.emit(progress)