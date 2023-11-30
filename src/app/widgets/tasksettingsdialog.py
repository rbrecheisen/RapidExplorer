from PySide6.QtWidgets import QDialog, QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit, QLabel

from widgets.tasksettingbooleanwidget import TaskSettingBooleanWidget


class TaskSettingsDialog(QDialog):
    def __init__(self, task: Task) -> None:
        super(TaskSettingsDialog, self).__init__()
        self._task = task
        self._taskSettingWidgets = {}
        self.initUi()

    def initUi(self) -> None:
        self._taskSettingWidgets = self.createTaskSettingWidgets()

    def createTaskSettingWiddgets(self) ->None:
        settings = self._task.settings()
        for setting in settings.all():
            if settings.isTypeIsBoolean(setting):
                widget = TaskSettingBooleanWidget()
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFileSet(setting):
                pass

            elif settings.isTypeFloatingPoint(setting):
                widget = QDoubleSpinBox(self)
                widget.setRange(setting.minimum(), setting.maximum())
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeInteger(setting):
                widget = QSpinBox(self)
                widget.setRange(setting.minimum(), setting.maximum())
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeOptionList(setting):
                pass

            elif settings.isTypeText(setting):
                pass

            else:
                raise RuntimeError(f'Unknown setting {setting.name()}')
        return self._taskSettingWidgets
    
    def createLabel(self, setting) -> QLabel:
        displayName = setting.displayName()
        if not setting.optional():
            displayName += '*'
        return QLabel(displayName)