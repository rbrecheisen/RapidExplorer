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
        return None, None

    def finalize(self) -> None:
        pass

    # def run(self) -> None:
    #     canceled = False
    #     manager = DataManager()

    #     # Prepare parameters, then run task
    #     inputFileSetName = self.parameter('inputFileSetName').value()
    #     inputFileSet = manager.fileSetByName(inputFileSetName)
    #     if inputFileSet is not None:
    #         outputFileSetPath = self.parameter('outputFileSetPath').value()
    #         outputFileSetName = self.parameter('outputFileSetName').value()
    #         if outputFileSetName is None:
    #             outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
    #         overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()

    #         # Already create output fileset directory here because we're writing new 
    #         # files inside the loop
    #         outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
    #         if overwriteOutputFileSet:
    #             if os.path.isdir(outputFileSetPath):
    #                 shutil.rmtree(outputFileSetPath)
    #         os.makedirs(outputFileSetPath, exist_ok=False)

    #         self.addInfo(f'Running task ({self.parameterValuesAsString()})')
    #         step = 0
    #         files = inputFileSet.files()
    #         nrSteps = len(files)
    #         for file in files:

    #             # Chec if the task should cancel
    #             if self.statusIsCanceling():
    #                 self.addInfo('Canceling task...')
    #                 canceled = True
    #                 break
                
    #             try:
    #                 p = pydicom.dcmread(file.path())
    #                 p.decompress()
    #                 outputFileName = file.name()
    #                 outputFilePath = os.path.join(outputFileSetPath, outputFileName)
    #                 p.save_as(outputFilePath)
    #                 # time.sleep(0.01)
    #             except pydicom.errors.InvalidDicomError:
    #                 self.addWarning(f'Skipping non-DICOM: {file.path()}')

    #             # Update progress for this iteration         
    #             self.updateProgress(step=step, nrSteps=nrSteps)
    #             step += 1

    #         # Finalize task
    #         manager.createFileSet(fileSetPath=outputFileSetPath)
    #         self.addInfo('Finished')
    #     else:
    #         self.addError(f'Input fileset {inputFileSetName} does not exist')

    #     # Determine task final status
    #     if canceled:
    #         self.setStatusCanceled()
    #     elif self.hasErrors():
    #         self.setStatusError()
    #     else:
    #         self.setStatusFinished()