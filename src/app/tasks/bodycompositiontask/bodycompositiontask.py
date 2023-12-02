import csv

from tasks.task import Task
from tasks.tasksignal import TaskSignal
from tasks.tasksettingfilepath import TaskSettingFilePath
from tasks.tasksettingfilesetpath import TaskSettingFileSetPath
from tasks.tasksettingtext import TaskSettingText
from tasks.tasksettingfileset import TaskSettingFileSet
from data.fileset import FileSet
from utils import createRandomName


class BodyCompositionTask(Task):
    def __init__(self) -> None:
        self.settings().add(TaskSettingFileSet(name='dicomFileSetName', displayName='DICOM File Set'))
        self.settings().add(TaskSettingFileSet(name='segmentationFileSetName', displayName='Segmentation File Set'))
        self.settings().add(TaskSettingFilePath(name='patientHeightsCsvFilePath', displayName='Patient Heights (*.csv)', optional=True))
        self.settings().add(TaskSettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(TaskSettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self.settings().add(TaskSettingFileSet(name='outputFileSet', displayName='Output File Set', visible=False))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        # DICOM files
        inputFileSetName = self.settings().setting(name='dicomFileSetName').value()
        inputFileSet = self._dataManager.fileSetByName(name=inputFileSetName)
        inputFilePaths = []
        for file in inputFileSet.files():
            inputFilePaths.append(file.path())
        # Segmentation files
        segmentationFileSetName = self.settings().setting(name='segmentationFileSetName').value()
        segmentationFileSet = self._dataManager.fileSetByName(name=segmentationFileSetName)
        segmentationFilePaths = []
        for file in segmentationFileSet.files():
            segmentationFilePaths.append(file)
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
        # Output file set
        outputFileSetPath = self.settings().setting(name='outputFileSetPath').value()
        outputFileSetName = self.settings().setting(name='outputFileSetName').value()
        if not outputFileSetName:
            outputFileSetName = createRandomName(prefix='output')        
        self.settings().setting(name='outputFileSetName').setValue(outputFileSetName)
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        self.settings().setting(name='outputFileSetPath').setValue(outputFileSetPath)
        os.makedirs(outputFileSetPath, exist_ok=False)

        #

        # Build output file set
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetPath)
        outputFileSet.setName(outputFileSetName)
        outputFileSet = self._dataManager.updateFileSet(fileSet=outputFileSet)
        self.settings().setting(name='outputFileSet').setValue(value=outputFileSet)        
        self.signal().finished.emit(outputFileSet)
        return outputFileSet
