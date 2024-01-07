import os
import time
import shutil
import pydicom
import pydicom.errors

from tasks.task import Task
from data.datamanager import DataManager
from logger import Logger

LOGGER = Logger()


class CheckDicomHeaderTask(Task):
    def __init__(self) -> None:
        super(CheckDicomHeaderTask, self).__init__()

    def run(self) -> None:
        canceled = False
        manager = DataManager()

        # Prepare parameters, then run task
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = manager.fileSetByName(inputFileSetName)
        if inputFileSet is not None:
            requiredAttributes = [x.strip() for x in self.parameter('requiredAttributes').value().split(',')]
            rows = self.parameter('rows').value()
            columns = self.parameter('columns').value()
            outputFileSetPath = self.parameter('outputFileSetPath').value()
            outputFileSetName = self.parameter('outputFileSetName').value()
            if outputFileSetName is None:
                outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
            overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()

            # Run task
            LOGGER.info(f'CheckDicomHeaderTask: running task ({self.parameterValuesAsString()})')
            step = 0
            dicomFilesOk = []
            files = inputFileSet.files()
            nrSteps = len(files) + 1 # Add final step to build output fileset
            for file in files:

                # Chec if the task should cancel
                if self.statusIsCanceling():
                    canceled = True
                    break
                try:

                    # Try reading file as DICOM (do not decompress because we don't read pixel data)
                    p = pydicom.dcmread(file.path(), stop_before_pixels=True)
                    
                    # Check if required attributes are present
                    allAttributesOk = True
                    for attribute in requiredAttributes:
                        if attribute not in p:
                            self.addError(f'Missing required attribute "{attribute}": {file.path()}')
                            allAttributesOk = False
                            break
                    if allAttributesOk:
                    
                        # Check if DICOM file has required rows and columns
                        rowsAndColumnsOk = True
                        if p.Rows != rows:
                            self.addError(f'rows={p.Rows}, should be {rows}')
                            rowsAndColumnsOk = False
                        if p.Columns != columns:
                            self.addError(f'rows={p.Columns}, should be {columns}')
                            rowsAndColumnsOk = False
                        if rowsAndColumnsOk:

                            # All is well, add file to final set
                            dicomFilesOk.append(file)
                        else:
                            pass
                    else:
                        pass
                except pydicom.errors.InvalidDicomError:
                    self.addError(f'Not valid DICOM: {file.path()}')       

                # Update progress for this iteration         
                self.updateProgress(step=step, nrSteps=nrSteps)
                step += 1

                # Wait a while...
                time.sleep(0)

            # Copy checked DICOM files to output fileset directory
            outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
            if overwriteOutputFileSet:
                if os.path.isdir(outputFileSetPath):
                    shutil.rmtree(outputFileSetPath)
            os.makedirs(outputFileSetPath, exist_ok=False)
            LOGGER.info(f'CheckDicomHeaderTask: writing checked DICOM files to {outputFileSetPath}...')
            for dicomFile in dicomFilesOk:
                shutil.copy(dicomFile.path(), outputFileSetPath)

            # Create output fileset
            manager.createFileSet(fileSetPath=outputFileSetPath)
            
            # Update final progress
            self.updateProgress(step=step, nrSteps=nrSteps)
        else:
            self.addError(f'Input fileset {inputFileSetName} does not exist')

        # Determine task final status
        if canceled:
            self.setStatusCanceled()
        elif self.hasErrors():
            self.setStatusError()
        else:
            self.setStatusFinished()