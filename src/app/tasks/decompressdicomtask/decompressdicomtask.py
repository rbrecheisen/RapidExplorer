import os
import shutil
import pydicom
import pydicom.errors

from tasks.task import Task
from data.filecontentcache import FileContentCache
from data.filecontent import FileContent
from logger import Logger

LOGGER = Logger()


class DecompressDicomTask(Task):
    def __init__(self) -> None:
        super(DecompressDicomTask, self).__init__()
        self._cache = FileContentCache()

    def execute(self) -> None:

        # Prepare parameters, then run task
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(inputFileSetName)
        if inputFileSet is not None:

            outputFileSetPath = self.parameter('outputFileSetPath').value()
            outputFileSetName = self.parameter('outputFileSetName').value()
            if outputFileSetName is None:
                outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)

            overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
            outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
            
            if overwriteOutputFileSet:
                if os.path.isdir(outputFileSetPath):
                    shutil.rmtree(outputFileSetPath)
            os.makedirs(outputFileSetPath, exist_ok=False)

            step = 0
            files = inputFileSet.files()
            nrSteps = len(files)
            for file in files:

                # Chec if the task should cancel
                if self.statusIsCanceled():
                    self.addInfo('Canceling task...')
                    break
                
                try:
                    # Try to load file content from cache first. If it's not available
                    # read it from disk
                    if self._cache.has(id=file.id()):
                        content = self._cache.get(id=file.id())
                        p = content.fileObject()
                    else:
                        p = pydicom.dcmread(file.path())
                        p.decompress()
                        self._cache.add(FileContent(file=file, fileObject=p))
                        
                    outputFileName = file.name()
                    outputFilePath = os.path.join(outputFileSetPath, outputFileName)
                    p.save_as(outputFilePath)
                except pydicom.errors.InvalidDicomError:
                    self.addWarning(f'Skipping non-DICOM: {file.path()}')

                # Update progress for this iteration         
                self.updateProgress(step=step, nrSteps=nrSteps)
                step += 1

            # Finalize task
            self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
            self.addInfo('Finished')
        else:
            self.addError(f'Input fileset {inputFileSetName} does not exist')