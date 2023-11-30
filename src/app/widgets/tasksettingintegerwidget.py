from PySide6.QtWidgets import QWidget, QSpinBox

from tasks.tasksetting import TaskSetting


class TaskSettingIntegerWidget(QSpinBox):
    def __init__(self, setting: TaskSetting, parent: QWidget=None) -> None:
        super(TaskSettingIntegerWidget, self).__init__(parent=parent)
        self._setting = setting
        self.valueChanged.connect(self.settingChanged)

    def setRange(self, minimum: int, maximum: int) -> None:
        self.setRange(minimum, maximum)

    def settingChanged(self, value: int) -> None:
        if value:
            self._setting.setValue(value)