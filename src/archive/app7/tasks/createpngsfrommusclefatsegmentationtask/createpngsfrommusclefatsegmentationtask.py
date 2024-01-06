import os
import shutil

from utils import createNameWithTimestamp, loadNumPyArray, convertDicomToNumPyArray, convertNumPyArrayToPngImage
from utils import AlbertaColorMap
from tasks.task import Task
from tasks.taskoutput import TaskOutput
from tasks.tasksignal import TaskSignal
from settings.settingfileset import SettingFileSet
from settings.settingfilesetpath import SettingFileSetPath
from settings.settingboolean import SettingBoolean
from settings.settinglabel import SettingLabel
from settings.settinginteger import SettingInteger
from settings.settingtext import SettingText
from data.fileset import FileSet
from data.pngfiletype import PngFileType
from data.allfiletype import AllFileType
from logger import Logger

LOGGER = Logger()

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
        setting = SettingInteger(name='windowCenter', displayName='Window Center', defaultValue=50)
        setting.setWidgetTypeSpinBox()
        self.settings().add(setting)
        setting = SettingInteger(name='windowWidth', displayName='Window Width', defaultValue=400)
        setting.setWidgetTypeSpinBox()
        self.settings().add(setting)
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
        LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() outputFileSetName={outputFileSetName}')
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() outputFileSetPath={outputFileSetPath}')
        os.makedirs(outputFileSetPath, exist_ok=False)
        # Get window center and width
        windowCenter = self.settings().setting(name='windowCenter').value()
        windowWidth = self.settings().setting(name='windowWidth').value()
        # DICOM files
        dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
        LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() dicomFileSetName={dicomFileSetName}')
        dicomFileSet = self.dataManager().fileSetByName(name=dicomFileSetName)
        for dicomFile in dicomFileSet.files():
            LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() Converting {dicomFile.path()} to NumPy array with windowCenter={windowCenter} and windowWidth={windowWidth}')
            numpyArray = convertDicomToNumPyArray(dicomFile.path(), windowCenter=windowCenter, windowWidth=windowWidth)
            pngImageFileName = os.path.split(dicomFile.path())[1] + '.png'
            convertNumPyArrayToPngImage(
                numpyArrayFilePathOrObject=numpyArray, 
                colorMap=None,
                outputDirectoryPath=outputFileSetPath,
                pngImageFileName=pngImageFileName,
            )
            LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() Converted DICOM to PNG {pngImageFileName}')
        # Do same for segmentations
        segmentationFileSetName = self.settings().setting(name='segmentationFileSetName').value()
        LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() segmentationFileSetName={segmentationFileSetName}')
        segmentationFileSet = self.dataManager().fileSetByName(name=segmentationFileSetName)
        for segmentationFile in segmentationFileSet.files():
            LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() Loading NumPy array from file {segmentationFile.path}')
            numpyArray = loadNumPyArray(segmentationFile.path())
            pngImageFileName = os.path.split(segmentationFile.path())[1] + '.png'
            convertNumPyArrayToPngImage(
                numpyArrayFilePathOrObject=numpyArray,
                colorMap=AlbertaColorMap(),
                outputDirectoryPath=outputFileSetPath,
                pngImageFileName=pngImageFileName,
            )
            LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() Converted segmentation to PNG {pngImageFileName}')
        # Copy original DICOM files?
        copyDicomFilesToOutputFileSet = self.settings().setting(name='copyDicomFilesToOutputFileSet').value()
        if copyDicomFilesToOutputFileSet:
            for dicomFile in dicomFileSet.files():
                shutil.copy(dicomFile.path(), outputFileSetPath)
                LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() Copied original DICOM {dicomFile.path()} to output file set')
        # Copy segmentation files?
        copySegmentationFilesToOutputFileSet = self.settings().setting(name='copySegmentationFilesToOutputFileSet').value()
        if copySegmentationFilesToOutputFileSet:
            for segmentationFile in segmentationFileSet.files():
                shutil.copy(segmentationFile.path(), outputFileSetPath)
                LOGGER.info(f'CreatePngsFromMuscleFatSegmentationTask.run() Copied original segmentation file {segmentationFile.path()} to output file set')
        # Use AllFileType if you copied original DICOM and segmentation files
        fileType = PngFileType
        if copyDicomFilesToOutputFileSet or copySegmentationFilesToOutputFileSet:
            fileType = AllFileType
        # Import output file set and notify listeners
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetPath, fileType=fileType)
        taskOutput = TaskOutput(fileSet=outputFileSet, errorInfo=[])
        self.signal().finished.emit(taskOutput)
        return taskOutput
