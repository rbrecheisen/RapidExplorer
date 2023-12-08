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
from tasks.bodycompositiontask.bodycompositioncalculator import BodyCompositionCalculator
from data.fileset import FileSet
from utils import createNameWithTimestamp

DESCRIPTION = """
This task calculates body composition metrics for segmentation masks created with MuscleFatSegmentationTask.
"""


class BodyCompositionTask(Task):
    NAME = 'BodyCompositionTask'

    def __init__(self) -> None:
        super(BodyCompositionTask, self).__init__()
        self.settings().add(SettingLabel(name='description', value=DESCRIPTION))
        self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='DICOM File Set'))
        self.settings().add(SettingFileSet(name='segmentationFileSetName', displayName='Segmentation File Set'))
        self.settings().add(SettingFilePath(name='patientHeightsCsvFilePath', displayName='Patient Heights (*.csv)', optional=True))
        self.settings().add(SettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(SettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self.settings().add(SettingBoolean(name='copySegmentationsToOutputFileSet', displayName='Copy Segmentation Files to Output File Set', defaultValue=True))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        # DICOM files
        dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
        dicomFileSet = self._dataManager.fileSetByName(name=dicomFileSetName)
        dicomFilePaths = []
        for file in dicomFileSet.files():
            dicomFilePaths.append(file.path())
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
        os.makedirs(outputFileSetPath, exist_ok=False)
        # Get setting to copy segmentation files or not
        copySegmentationsToOutputFileSet = self.settings().setting(name='copySegmentationsToOutputFileSet').value()
        # Determine nr. stepts required for processing
        self.setNrSteps(len(dicomFilePaths))
        # Calculate scores
        calculator = BodyCompositionCalculator(parentTask=self)
        calculator.setDicomFilePaths(dicomFilePaths=dicomFilePaths)
        calculator.setSegmentationFilePaths(segmentationFilePaths=segmentationFilePaths)
        calculator.setPatientHeights(patientHeights=patientHeights)
        calculator.execute()
        df = calculator.as_df()
        csvFilePath = os.path.join(outputFileSetPath, createNameWithTimestamp('scores') + '.csv')
        df.to_csv(csvFilePath, index=False)
        # Copy segmentation files to output file set if necessary
        if copySegmentationsToOutputFileSet:
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