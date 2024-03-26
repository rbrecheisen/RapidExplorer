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
        step = 0
        dicomFilesOk = []
        files = inputFileSet.files()
        nrSteps = len(files)
        for file in files:
            try:
                p = pydicom.dcmread(file.path(), stop_before_pixels=True)
                allAttributesOk = True
                for attribute in requiredAttributes:
                    if attribute not in p:
                        LOGGER.warning(f'{file.path()}: attribute "{attribute}" not present')
                        allAttributesOk = False
                        break
                if allAttributesOk:
                    rowsAndColumnsOk = True
                    if p.Rows != rows:
                        LOGGER.warning(f'{file.path()}: nr. rows should be {rows} but is {p.Rows}')
                        rowsAndColumnsOk = False
                    if p.Columns != columns:
                        LOGGER.warning(f'{file.path()}: Nr. columns should be {columns} but is {p.Columns}')
                        rowsAndColumnsOk = False
                    if rowsAndColumnsOk:
                        dicomFilesOk.append(file)
                    else:
                        pass
                else:
                    pass
            except pydicom.errors.InvalidDicomError:
                LOGGER.warning(f'{file.path()} is not a valid DICOM file')
            self.updateProgress(step=step, nrSteps=nrSteps)
            step += 1
        LOGGER.info(f'Building output fileset...')
        for dicomFile in dicomFilesOk:
            shutil.copy(dicomFile.path(), outputFileSetPath)        
        self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
