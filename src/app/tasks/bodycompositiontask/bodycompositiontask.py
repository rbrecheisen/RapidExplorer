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
        self.settings().add(TaskSettingFileSet(name='dicomFileSet', displayName='DICOM File Set'))
        self.settings().add(TaskSettingFileSet(name='segmentationFileSet', displayName='Segmentation File Set'))
        self.settings().add(TaskSettingFilePath(name='patientHeightCsvFilePath', displayName='Patient Heights (*.csv)', optional=True))
        self.settings().add(TaskSettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(TaskSettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self.settings().add(TaskSettingFileSet(name='outputFileSet', displayName='Output File Set', visible=False))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        inputFileSetName = self.settings().setting(name='dicomFileSet').value()
        inputFileSet = self._dataManager.fileSetByName(name=inputFileSetName)
        inputFilePaths = []
        for file in inputFileSet.files():
            inputFilePaths.append(file.path())
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
