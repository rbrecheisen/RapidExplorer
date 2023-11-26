from PySide6.QtCore import QRunnable
from PySide6.QtWidgets import QDialog

from barbell2_bodycomp import MuscleFatSegmentator, BodyCompositionCalculator
from barbell2_bodycomp.convert import npy2png, dcm2npy

from plugins.tasks.task import Task
from plugins.tasks.tasktextsetting import TaskTextSetting
from plugins.tasks.taskfilesetselectorsetting import TaskFileSetSelectorSetting
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.filecache import FileCache
from data.datamanager import DataManager


class TaskRunner(QRunnable):
    def __init__(self, task) -> None:
        super(TaskRunner, self).__init__()
        self._task = task
        self._cache = FileCache()
        self._dataManager = DataManager()

    def task(self):
        return self._task
    
    def cache(self) -> FileCache:
        return self._cache

    def dataManager(self) -> DataManager:
        return self._dataManager


class L3AutoSegmentationTaskRunner(TaskRunner):
    def __init__(self, task) -> None:
        super(L3AutoSegmentationTaskRunner, self).__init__(task=task)

    def run(self) -> None:

        # Collect data
        inputFileSet = self.task().setting('inputFileSet').value()
        inputFileSetFiles = []
        for registeredFileModel in inputFileSet.registeredFileModels:
            file = self.cache().get(registeredFileModel.id)
            if not file:
                raise RuntimeError(f'File {registeredFileModel.path} not in file cache')
            inputFileSetFiles.append(registeredFileModel.path)

        tensorFlowModelFilesFileSet = self.task().setting('tensorFlowModelFileSet').value()
        tensorFlowModelFilesFileSetFiles = []
        for registeredFileModel in tensorFlowModelFilesFileSet.registeredFileModels:
            file = self.cache().get(registeredFileModel.id)
            if not file:
                raise RuntimeError(f'File {registeredFileModel.path} not in file cache')
            tensorFlowModelFilesFileSetFiles.append(registeredFileModel.path)

        # Run muscle/fat segmentator        
        segmentator = MuscleFatSegmentator()
        segmentator.input_files = inputFileSetFiles
        segmentator.model_files = tensorFlowModelFilesFileSetFiles
        segmentator.mode = MuscleFatSegmentator.ARGMAX
        raise RuntimeError('How to deal with segmentator.output_directory!')
        segmentator.output_directory = output_dataset.data_dir
        segmentation_files = segmentator.execute()        
        for f in segmentation_files:
            print(f)


class L3AutoSegmentationTask(Task):
    def __init__(self) -> None:
        super(L3AutoSegmentationTask, self).__init__(name='L3 Auto-Segmentation')
        self.addSetting(TaskFileSetSelectorSetting(name='inputFileSet', displayName='Input File Set'))
        self.addSetting(TaskFileSetSelectorSetting(name='tensorFlowModelFileSet', displayName='TensorFlow Model File Set'))
        self.addSetting(TaskTextSetting(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self._outputData = None

    def run(self):
        runner = L3AutoSegmentationTaskRunner(task=self)
        runner.run()

    def outputData(self) -> RegisteredMultiFileSetModel:
        return self._outputData