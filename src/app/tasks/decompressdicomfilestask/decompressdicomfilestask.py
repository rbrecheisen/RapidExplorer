import os
import zipfile

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
        self.settings().add(SettingFileSetPath(name='outputDirectoryPath', displayName='Output Directory Path'))
        self.settings().add(SettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self.settings().add(SettingBoolean(name='overwritePreviousOutputFileSet', displayName='Overwrite Previous Output File Set', defaultValue=True))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        # # Collect input settings
        # inputFileSetName = self.settings().setting(name='inputFileSetName').value()
        # inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
        # outputDirectoryPath = self.settings().setting(name='outputDirectoryPath').value()
        # zipFileName = createNameWithTimestamp(inputFileSet.name()) + '.zip'
        # # Create ZIP file
        # outputZipFilePath = os.path.join(outputDirectoryPath, zipFileName)
        # LOGGER.info(f'CreateArchiveTask.run() outputZipFilePath={outputZipFilePath}')
        # with zipfile.ZipFile(outputZipFilePath, 'w') as zipObj:
        #     for file in inputFileSet.files():
        #         LOGGER.info(f'CreateArchiveTask.run() adding {file.path()} to ZIP archive...')
        #         zipObj.write(file.path(), arcname=os.path.basename(file.path()))
        # # Create output fileset
        # outputFileSet = self.dataManager().importFileSet(fileSetPath=outputDirectoryPath, fileType=ZipFileType)
        # taskOutput = TaskOutput(fileSet=outputFileSet, errorInfo=[])
        # LOGGER.info(f'CreateArchiveTask.run() created output {taskOutput}')
        # self.signal().finished.emit(taskOutput)
        # return taskOutput
        raise RuntimeError('Implement this task!')
        return None