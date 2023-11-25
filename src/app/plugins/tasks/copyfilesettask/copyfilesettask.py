import os
import shutil

from plugins.tasks.task import Task
from data.filecache import FileCache
from data.allfiletype import AllFileType
from data.datamanager import DataManager
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class CopyFileSetTask(Task):
    def __init__(self) -> None:
        super(CopyFileSetTask, self).__init__(name='Copy File Set')
        self._dataManager = DataManager()
        self._dataManager.signal().progress.connect(self._updateProgress)
        self._outputData = None

    def run(self) -> None:
        # Copies fileset including SQL registration
        if self.hasData('source'):
            source = self.data('source')
            targetDirectory = self.parameter('targetDirectory')
            if os.path.isdir(targetDirectory):
                raise RuntimeError(f'Target directory {targetDirectory} already exists')
            os.makedirs(targetDirectory, exist_ok=False)
            # Copy files from source data to target directory
            # Each file in source must be in file cache for it to be copied
            cache = FileCache()
            for registeredFileModel in source.registeredFileModels:
                if cache.has(registeredFileModel.id):
                    shutil.copy(registeredFileModel.path, targetDirectory)
                    print(f'Copied {registeredFileModel.path} to {targetDirectory}')
            self._dataManager.importFileSet(targetDirectory, fileType=AllFileType())

    def outputData(self) -> RegisteredMultiFileSetModel:
        return self._outputData

    def _updateProgress(self, progress) -> None:
        if progress == 100:
            self._outputData = self._dataManager.data()
            print('Data copied')