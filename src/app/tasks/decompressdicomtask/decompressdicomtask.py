import os
import shutil

from typing import List, Union

from tasks.task import Task
from tasks.taskworkitem import TaskWorkItem
from tasks.decompressdicomtask.decompressdicomtaskworkitem import DecompressDicomTaskWorkItem
from logger import Logger

LOGGER = Logger()


class DecompressDicomTask(Task):
    def __init__(self) -> None:
        super(DecompressDicomTask, self).__init__()
        self._outputFileSetPath = None

    def prepareWorkItems(self) -> Union[List[TaskWorkItem], str]:
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(inputFileSetName)
        if inputFileSet:
            outputFileSetPath = self.parameter('outputFileSetPath').value()
            outputFileSetName = self.parameter('outputFileSetName').value()
            if outputFileSetName is None:
                outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
            outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
            overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
            if overwriteOutputFileSet:
                if os.path.isdir(outputFileSetPath):
                    shutil.rmtree(outputFileSetPath)
            os.makedirs(outputFileSetPath, exist_ok=False)
            workItems = []
            for file in inputFileSet.files():
                outputFilePath = os.path.join(outputFileSetPath, file.name())
                workItem = DecompressDicomTaskWorkItem(inputFilePath=file.path(), outputFilePath=outputFilePath)
                workItems.append(workItem)
            return workItems, outputFileSetPath
        else:
            self.addError(f'Input fileset {inputFileSetName} does not exist')

        # Determine task final status
        if canceled:
            self.setStatusCanceled()
        elif self.hasErrors():
            self.setStatusError()
        else:
            self.setStatusFinished()