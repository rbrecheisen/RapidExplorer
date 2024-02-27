import os
import shutil
import pydicom
import pydicom.errors

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.data.filecontentcache import FileContentCache
from mosamaticdesktop.utils import readFromCache, writeToCache
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class DecompressDicomTask(Task):
    def __init__(self) -> None:
        super(DecompressDicomTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Decompresses JPEG200-compressed DICOM files for use in Slice-o-matic.'
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set Name',
        )
        self.addPathParameter(
            name='outputFileSetPath',
            labelText='Output File Set Path',
        )
        self.addTextParameter(
            name='outputFileSetName',
            labelText='Output File Set Name',
            optional=True,
        )
        self.addBooleanParameter(
            name='overwriteOutputFileSet',
            labelText='Overwrite Output File Set',
            defaultValue=True,
        )
        self._cache = FileContentCache()

    def execute(self) -> None:
        # Prepare input parameters
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(inputFileSetName)
        outputFileSetPath = self.parameter('outputFileSetPath').value()
        outputFileSetName = self.parameter('outputFileSetName').value()
        if outputFileSetName is None:
            outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)

        overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        
        if overwriteOutputFileSet:
            if os.path.isdir(outputFileSetPath):
                shutil.rmtree(outputFileSetPath)
        os.makedirs(outputFileSetPath, exist_ok=True)

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
                content = readFromCache(file=file)
                if not content:
                    p = pydicom.dcmread(file.path())
                    p.decompress()
                    content = writeToCache(file, p)
                p = content.fileObject()

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