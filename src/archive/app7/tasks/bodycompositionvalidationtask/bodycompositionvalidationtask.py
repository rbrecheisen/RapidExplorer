import os
import csv
import shutil

from tasks.task import Task
from tasks.taskoutput import TaskOutput
from tasks.tasksignal import TaskSignal
from settings.settingfilepath import SettingFilePath
from settings.settingfilesetpath import SettingFileSetPath
from settings.settingtext import SettingText
from settings.settingfileset import SettingFileSet
from settings.settingboolean import SettingBoolean
from settings.settinglabel import SettingLabel
from tasks.bodycompositionvalidationtask.bodycompositionvalidationcalculator import BodyCompositionValidationCalculator
from data.fileset import FileSet
from utils import createNameWithTimestamp
from logger import Logger

LOGGER = Logger()

DESCRIPTION = """
This task validates body composition using TAG files.
"""


class BodyCompositionValidationTask(Task):
    NAME = 'BodyCompositionValidationTask'

    def __init__(self) -> None:
        super(BodyCompositionValidationTask, self).__init__()
        self.settings().add(SettingLabel(name='description', value=DESCRIPTION))
        self.settings().add(SettingFileSet(name='dicomAndTagFileSetName', displayName='DICOM and TAG File Set'))
        self.settings().add(SettingFileSet(name='segmentationFileSetName', displayName='Segmentation File Set'))
        self.settings().add(SettingFilePath(name='patientHeightsCsvFilePath', displayName='Patient Heights (*.csv)', optional=True))
        self.settings().add(SettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(SettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self.settings().add(SettingBoolean(name='copyTagAndSegmentationFilesToOutputFileSet', displayName='Copy TAG and Segmentation Files to Output File Set', defaultValue=False))
        self.settings().add(SettingBoolean(name='overwritePreviousOutputFileset', displayName='Overwrite Previous Output File Set', defaultValue=True))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        # DICOM files
        dicomAndTagFileSetName = self.settings().setting(name='dicomAndTagFileSetName').value()
        dicomAndTagFileSet = self._dataManager.fileSetByName(name=dicomAndTagFileSetName)
        dicomAndTagFilePaths = []
        for file in dicomAndTagFileSet.files():
            dicomAndTagFilePaths.append(file.path())
        # Segmentation files
        segmentationFileSetName = self.settings().setting(name='segmentationFileSetName').value()
        segmentationFileSet = self._dataManager.fileSetByName(name=segmentationFileSetName)
        segmentationFilePaths = []
        for file in segmentationFileSet.files():
            if file.path().endswith('.npy'):
                segmentationFilePaths.append(file.path())
        # Patient heights CSV (use csv package to load)
        patientHeights = None
        patientHeightsCsvFilePath = self.settings().setting(name='patientHeightsCsvFilePath').value()
        if patientHeightsCsvFilePath:
            patientHeights = {}
            with open(patientHeightsCsvFilePath, 'r') as f:
                reader = csv.reader(f)                
                for row in reader:
                    # If both row values are strings, this is probably the header
                    if isinstance(row[0], str) and isinstance(row[1], str):
                        next(reader)
                        continue
                    patientHeights[row[0]] = float(row[1])
        # Determine output file set settings
        outputFileSetPath = self.settings().setting(name='outputFileSetPath').value()
        outputFileSetName = self.settings().setting(name='outputFileSetName').value()
        if not outputFileSetName:
            outputFileSetName = createNameWithTimestamp(prefix='output')
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        # Get setting to overwrite previous output
        overwritePreviousOutputFileset = self.settings().setting(name='overwritePreviousOutputFileset').value()
        LOGGER.info(f'BodyCompositionValidationTask.execute() overwritePreviousOutputFileSet={overwritePreviousOutputFileset}')
        os.makedirs(outputFileSetPath, exist_ok=overwritePreviousOutputFileset)
        # Get setting to copy segmentation files or not
        copyTagAndSegmentationFilesToOutputFileSet = self.settings().setting(name='copyTagAndSegmentationFilesToOutputFileSet').value()
        LOGGER.info(f'BodyCompositionValidationTask.execute() copyTagAndSegmentationFilesToOutputFileSet={copyTagAndSegmentationFilesToOutputFileSet}')
        # Determine nr. stepts required for processing
        self.setNrSteps(len(dicomAndTagFilePaths))
        # Calculate scores
        calculator = BodyCompositionValidationCalculator(parentTask=self)
        calculator.setDicomAndTagFilePaths(dicomAndTagFilePaths=dicomAndTagFilePaths)
        calculator.setSegmentationFilePaths(segmentationFilePaths=segmentationFilePaths)
        calculator.setPatientHeights(patientHeights=patientHeights)
        calculator.execute()
        df = calculator.as_df()
        csvFilePath = os.path.join(outputFileSetPath, createNameWithTimestamp('scores') + '.csv')
        df.to_csv(csvFilePath, index=False)
        # Copy segmentation files to output file set if necessary
        if copyTagAndSegmentationFilesToOutputFileSet:
            for file in dicomAndTagFilePaths:
                if file.endswith('.tag'):
                    shutil.copy(file, outputFileSetPath)
            for file in segmentationFilePaths:
                shutil.copy(file, outputFileSetPath)
        # Build new output file set
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetPath)
        taskOutput = TaskOutput(fileSet=outputFileSet, errorInfo=[])
        self.signal().finished.emit(taskOutput)
        return taskOutput

    def calculatorProgress(self, progress) -> None:
        progress = int((progress + 1) / (self._nrSteps + 1) * 100)
        self.signal().progress.emit(progress)