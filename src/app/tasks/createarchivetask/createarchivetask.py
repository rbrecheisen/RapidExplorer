from tasks.task import Task
from tasks.tasksignal import TaskSignal
from settings.settingfileset import SettingFileSet
from settings.settingfilesetpath import SettingFileSetPath
from settings.settingtext import SettingText


class CreateArchiveTask(Task):
    NAME = 'CreateArchiveTask'

    def __init__(self) -> None:
        super(CreateArchiveTask, self).__init__()
        self.settings().add(SettingFileSet(name='inputFileSetName', displayName='File Set to Compress'))
        self.settings().add(SettingFileSetPath(name='outputDirectoryPath', displayName='Output Directory Path'))
        self.settings().add(SettingText(name='zipFileName', displayName='ZIP File Name', optional=True))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal
    
    def run(self) -> FileSet:
        inputFileSetName = self.settings().setting(name='inputFileSetName').value()
        if inputFileSetName:
            inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
            raise RuntimeError('Continue here!')