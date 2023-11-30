from PySide6.QtWidgets import QWidget, QComboBox

from tasks.tasksetting import TaskSetting


class TaskSettingBooleanWidget(QComboBox):
    def __init__(self, setting: TaskSetting, parent: QWidget=None) -> None:
        super(TaskSettingBooleanWidget, self).__init__(parent=parent)
        self._setting = setting
        self.currentIndexChanged.connect(self.settingChanged)
        self.addItems([None, 'True', 'False'])

    def settingChanged(self, index: int) -> None:
        value = self.currentText()
        if value:
            value = True if value == 'True' else False
            self._setting.setValue(value)