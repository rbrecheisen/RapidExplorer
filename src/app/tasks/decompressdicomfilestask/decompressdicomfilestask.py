import os
import pydicom
import pydicom.errors

from utils import createNameWithTimestamp
from tasks.task import Task
from tasks.taskoutput import TaskOutput
from tasks.tasksignal import TaskSignal
from settings.settingfileset import SettingFileSet
from settings.settingfilesetpath import SettingFileSetPath
from settings.settinglabel import SettingLabel
from settings.settingtext import SettingText
from settings.settingboolean import SettingBoolean
from data.fileset import FileSet
from data.zipfiletype import ZipFileType
from logger import Logger

LOGGER = Logger()

DESCRIPTION = """
This task decompresses DICOM files compressed in JPEG2000.
"""


class DecompressDicomFilesTask(Task):
    NAME = 'DecompressDicomFilesTask'

    def __init__(self) -> None:
        super(DecompressDicomFilesTask, self).__init__()
        self.settings().add(SettingLabel(name='description', value=DESCRIPTION))
        self.settings().add(SettingFileSet(name='inputFileSetName', displayName='DICOM Input File Set to Decompress'))
        self.settings().add(SettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(SettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self.settings().add(SettingBoolean(name='overwritePreviousOutputFileSet', displayName='Overwrite Previous Output File Set', defaultValue=True))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        inputFileSetName = self.settings().setting(name='inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
        inputFilePaths = []
        for file in inputFileSet.files():
            inputFilePaths.append(file.path())
        outputFileSetPath = self.settings().setting(name='outputFileSetPath').value()
        outputFileSetName = self.settings().setting(name='outputFileSetName').value()
        if not outputFileSetName:
            outputFileSetName = createNameWithTimestamp(prefix='output')        
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        overwritePreviousOutputFileSet = self.settings().setting(name='overwritePreviousOutputFileSet').value()
        os.makedirs(outputFileSetPath, exist_ok=overwritePreviousOutputFileSet)
        # Set nr of steps
        self.setNrSteps(len(inputFilePaths))
        # Decompress files (if DICOM)
        for filePath in inputFilePaths:
            try:
                p = pydicom.dcmread(filePath)
                p.decompress()
                fileName = os.path.split(filePath)[1]
                outputFilePath = os.path.join(outputFileSetPath, fileName)
                p.save_as(outputFilePath)
            except pydicom.errors.InvalidDicomError:
                pass
        # Build output file set
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetPath)
        taskOutput = TaskOutput(fileSet=outputFileSet, errorInfo=[])
        self.signal().finished.emit(taskOutput)
        return taskOutput