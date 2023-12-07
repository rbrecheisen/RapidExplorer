import os

from utils import createNameWithTimestamp
from tasks.task import Task
from tasks.tasksignal import TaskSignal
from settings.settingfileset import SettingFileSet
from settings.settingfilesetpath import SettingFileSetPath
from settings.settinglabel import SettingLabel
from data.fileset import FileSet

DESCRIPTION = """
This task generates PNG images of DICOM files and segmentation masks.
"""


class CreatePngsFromMuscleFatSegmentationTask(Task):
    NAME = 'CreatePngsFromMuscleFatSegmentationTask'

    def __init__(self) -> None:
        super(CreatePngsFromMuscleFatSegmentationTask, self).__init__()
        self.settings().add(SettingLabel(name='description', value=DESCRIPTION))
        self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='DICOM File Set'))
        self.settings().add(SettingFileSet(name='segmentationFileSetName', displayName='Segmentation File Set'))
        self.settings().add(SettingFileSetPath(name='outputDirectoryPath', displayName='Output Directory Path'))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        # # Collect input settings
        dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
        dicomFileSet = self.dataManager().fileSetByName(name=dicomFileSetName)
        
        segmentationFileSetName = self.settings().setting(name='segmentationFileSetName').value()
        segmentationFileSet = self.dataManager().fileSetByName(name=segmentationFileSetName)
        outputDirectoryPath = self.settings().setting(name='outputDirectoryPath').value()
        # # Create output fileset
        # outputFileSet = self.dataManager().importFileSet(fileSetPath=outputDirectoryPath, fileType=ZipFileType)
        # self.signal().finished.emit(outputFileSet)
        # return outputFileSet
        pass