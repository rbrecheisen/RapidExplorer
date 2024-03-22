import os
import shutil
import pydicom
import pydicom.errors

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class CheckDicomHeaderTask(Task):
    def __init__(self) -> None:
        super(CheckDicomHeaderTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Check DICOM headers',
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set',
        )
        self.addTextParameter(
            name='extensionsToIgnore',
            labelText='Extensions to Ignore (comma-separated)',
            defaultValue='tag'
        )
        self.addTextParameter(
            name='requiredAttributes',
            labelText='Required DICOM Attributes',
            defaultValue='Rows, Columns, PixelSpacing',
        )
        self.addIntegerParameter(
            name='rows',
            labelText='Rows',
            defaultValue=512,
            minimum=0,
            maximum=1024,
        )
        self.addIntegerParameter(
            name='columns',
            labelText='Columns',
            defaultValue=512,
            minimum=0,
            maximum=1024,
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

    def execute(self) -> None:
        # Prepare parameters, then run task
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(inputFileSetName)
        requiredAttributes = [x.strip() for x in self.parameter('requiredAttributes').value().split(',')]
        rows = self.parameter('rows').value()
        columns = self.parameter('columns').value()
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

        # Run task
        step = 0
        dicomFilesOk = []
        files = inputFileSet.files()
        nrSteps = len(files)
        for file in files:

            # Chec if the task should cancel
            if self.statusIsCanceled():
                self.addInfo('Canceling task...')
                break
            try:
                # Try reading file as DICOM (do not decompress because we don't read pixel data)
                # Don't use the cache because we're not reading pixels
                p = pydicom.dcmread(file.path(), stop_before_pixels=True)
                
                # Check if required attributes are present
                allAttributesOk = True
                for attribute in requiredAttributes:
                    if attribute not in p:
                        self.addError(f'{file.path()}: Missing required attribute "{attribute}"')
                        allAttributesOk = False
                        break
                if allAttributesOk:
                
                    # Check if DICOM file has required rows and columns
                    rowsAndColumnsOk = True
                    if p.Rows != rows:
                        self.addError(f'{file.path()}: rows={p.Rows}, should be {rows}')
                        rowsAndColumnsOk = False
                    if p.Columns != columns:
                        self.addError(f'{file.path()}: columns={p.Columns}, should be {columns}')
                        rowsAndColumnsOk = False
                    if rowsAndColumnsOk:
                        dicomFilesOk.append(file)
                    else:
                        pass
                else:
                    pass
            except pydicom.errors.InvalidDicomError:
                self.addWarning(f'{file.path()}: Skipping non-DICOM')

            # Update progress for this iteration         
            self.updateProgress(step=step, nrSteps=nrSteps)
            step += 1

        # Copy checked DICOM files to output fileset directory
        for dicomFile in dicomFilesOk:
            shutil.copy(dicomFile.path(), outputFileSetPath)
        
        self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
        self.addInfo('Finished')
