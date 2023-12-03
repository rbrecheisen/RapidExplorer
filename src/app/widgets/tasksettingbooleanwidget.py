from PySide6.QtWidgets import QWidget, QComboBox

from tasks.tasksetting import TaskSetting


class TaskSettingBooleanWidget(QComboBox):
    def __init__(self, setting: TaskSetting, parent: QWidget=None) -> None:
        super(TaskSettingBooleanWidget, self).__init__(parent=parent)
        self._setting = setting
        self.currentIndexChanged.connect(self.settingChanged)
        self.addItems(['True', 'False'])
        if self._setting.defaultValue():
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(1)

    def settingChanged(self, index: int) -> None:
        value = self.currentText()
        value = True if value == 'True' else False
        self._setting.setValue(value)