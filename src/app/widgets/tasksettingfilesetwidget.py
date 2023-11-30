from PySide6.QtWidgets import QWidget, QComboBox

from data.datamanager import DataManager
from tasks.tasksetting import TaskSetting


class TaskSettingFileSetWidget(QComboBox):
    def __init__(self, setting: TaskSetting, parent: QWidget=None) -> None:
        super(TaskSettingFileSetWidget, self).__init__(parent=parent)
        self._setting = setting
        self._dataManager = DataManager()
        self.currentIndexChanged.connect(self.settingChanged)
        self.initUi()

    def initUi(self) -> None:
        self.addItem(None)
        for fileSet in self._dataManager.fileSets():
            self.addItem(fileSet.name())

    def settingChanged(self, index: int) -> None:
        value = self.currentText()
        if value:
            self._setting.setValue(value)