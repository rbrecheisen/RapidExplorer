import os

from utils import createNameWithTimestamp, convertDicomToNumPyArray, convertNumPyArrayToPngImage, AlbertaColorMap
from tasks.task import Task
from tasks.taskoutput import TaskOutput
from tasks.tasksignal import TaskSignal
from settings.settingfileset import SettingFileSet
from settings.settingfilesetpath import SettingFileSetPath
from settings.settingboolean import SettingBoolean
from settings.settinglabel import SettingLabel
from settings.settingtext import SettingText
from data.fileset import FileSet
from data.pngfiletype import PngFileType

DESCRIPTION = """
This task generates PNG images of DICOM files and segmentation masks.
"""


class CreatePngsFromMuscleFatSegmentationTask(Task):
    NAME = 'CreatePngsFromMuscleFatSegmentationTask'

    def __init__(self) -> None:
        super(CreatePngsFromMuscleFatSegmentationTask, self).__init__()
        self.settings().add(SettingLabel(name='description', value=DESCRIPTION))
        self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='DICOM File Set'))
        self.settings().add(SettingBoolean(name='copyDicomFilesToOutputFileSet', displayName='Copy DICOM Files to Output File Set'))
        self.settings().add(SettingFileSet(name='segmentationFileSetName', displayName='Segmentation File Set'))
        self.settings().add(SettingBoolean(name='copySegmentationFilesToOutputFileSet', displayName='Copy Segmentation Files to Output File Set'))
        self.settings().add(SettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(SettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        # Collect input settings
        outputFileSetPath = self.settings().setting(name='outputFileSetPath').value()
        outputFileSetName = self.settings().setting(name='outputFileSetName').value()
        if not outputFileSetName:
            outputFileSetName = createNameWithTimestamp(prefix='output')
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        os.makedirs(outputFileSetPath, exist_ok=False)
        # DICOM files
        dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
        dicomFileSet = self.dataManager().fileSetByName(name=dicomFileSetName)
        for dicomFile in dicomFileSet.files():
            numpyArray = convertDicomToNumPyArray(dicomFile.path(), windowCenter=50, windowWidth=400)
            convertNumPyArrayToPngImage(
                numpyArrayFilePathOrObject=numpyArray, 
                colorMap=AlbertaColorMap(),
                outputDirectoryPath=outputFileSetPath,
                pngImageFileName=os.path.split(dicomFile.path())[1] + '.png',
            )
        # # Do same for segmentations
        # segmentationFileSetName = self.settings().setting(name='segmentationFileSetName').value()
        # segmentationFileSet = self.dataManager().fileSetByName(name=segmentationFileSetName)

        # Copy original DICOM files?

        # Copy segmentation files?

        # Create output fileset
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetPath, fileType=PngFileType)
        taskOutput = TaskOutput(fileSet=outputFileSet, errorInfo=[])
        self.signal().finished.emit(taskOutput)
        return taskOutput
