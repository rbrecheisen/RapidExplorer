from PySide6.QtWidgets import QDialog, QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit


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
                widget = QComboBox(self)
                widget.addItems([None, 'True', 'False'])
                self._taskSettingWidgets[setting.name()] = (setting, widget)

            elif settings.isTypeFileSet(setting):
                pass

            elif settings.isTypeFloatingPoint(setting):
                widget = QDoubleSpinBox(self)
                widget.setRange(setting.minimum(), setting.maximum())
                

            elif settings.isTypeInteger(setting):
                widget = QSpinBox(self)
                widget.setRange(setting.minimum(), setting.maximum())
                self._taskSettingWidgets[setting.name()] = (setting, widget)

            elif settings.isTypeOptionList(setting):
                pass

            elif settings.isTypeText(setting):
                pass

            else:
                raise RuntimeError(f'Unknown setting {setting.name()}')
        return self._taskSettingWidgets