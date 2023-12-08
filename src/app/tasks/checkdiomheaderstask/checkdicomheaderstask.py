import pydicom

from tasks.task import Task
from tasks.tasksignal import TaskSignal
from data.fileset import FileSet
from settings.settinglabel import SettingLabel
from settings.settingfileset import SettingFileSet
from settings.settingfilepath import SettingFilePath

DESCRIPTION = """
This task checks DICOM headers to see whether all attributes are correct for MuscleFatSegmentationTask
"""


class CheckDicomHeadersTask(Task):
    def __init__(self) -> None:
        super(CheckDicomHeadersTask, self).__init__()
        self.settings().add(SettingLabel(name='description', value=DESCRIPTION))
        self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='DICOM File Set'))
        self.settings().add(SettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal

    def run(self) -> FileSet:
        dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
        dicomFileSet = self.dataManager().fileSetByName(name=dicomFileSetName)
        for dicomFile in dicomFileSet.files():
            p = pydicom.dcmread(dicomFile.path())
            