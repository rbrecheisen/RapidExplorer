import os
import zipfile

from utils import createNameWithTimestamp
from tasks.task import Task
from tasks.tasksignal import TaskSignal
from settings.settingfileset import SettingFileSet
from settings.settingfilesetpath import SettingFileSetPath
# from settings.settingtext import SettingText
from data.fileset import FileSet
from data.zipfiletype import ZipFileType


class CreateArchiveTask(Task):
    NAME = 'CreateArchiveTask'

    def __init__(self) -> None:
        super(CreateArchiveTask, self).__init__()
        self.settings().add(SettingFileSet(name='inputFileSetName', displayName='File Set to Compress'))
        self.settings().add(SettingFileSetPath(name='outputDirectoryPath', displayName='Output Directory Path'))
        # self.settings().add(SettingText(name='zipFileName', displayName='ZIP File Name', optional=True))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        # Collect input settings
        inputFileSetName = self.settings().setting(name='inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
        outputDirectoryPath = self.settings().setting(name='outputDirectoryPath').value()
        zipFileName = createNameWithTimestamp(inputFileSet.name()) + '.zip'
        # Create ZIP file
        outputZipFilePath = os.path.join(outputDirectoryPath, zipFileName)
        with zipfile.ZipFile(outputZipFilePath, 'w') as zipObj:
            for file in inputFileSet.files():
                zipObj.write(file.path(), arcname=os.path.basename(file.path()))
        # Create output fileset
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputDirectoryPath, fileType=ZipFileType)
        self.signal().finished.emit(outputFileSet)
        return outputFileSet