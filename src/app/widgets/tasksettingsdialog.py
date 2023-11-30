from PySide6.QtWidgets import QDialog, QLabel, QPushButton

from widgets.tasksettingbooleanwidget import TaskSettingBooleanWidget
from widgets.tasksettingfilesetwidget import TaskSettingFileSetWidget
from widgets.tasksettingfloatingpointwidget import TaskSettingFloatingPointWidget
from widgets.tasksettingintegerwidget import TaskSettingIntegerWidget
from widgets.tasksettingoptionlistwidget import TaskSettingOptionListWidget
from widgets.tasksettingtextwidget import TaskSettingTextWidget


class TaskSettingsDialog(QDialog):
    def __init__(self, task: Task) -> None:
        super(TaskSettingsDialog, self).__init__()
        self._task = task
        self._taskSettingWidgets = {}
        self.initUi()

    def initUi(self) -> None:
        self._taskSettingWidgets = self.createTaskSettingWidgets()

    def createTaskSettingWidgets(self) ->None:
        settings = self._task.settings()
        for setting in settings.all():
            if settings.isTypeIsBoolean(setting):
                widget = TaskSettingBooleanWidget(parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFileSet(setting):
                widget = TaskSettingFileSetWidget(parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFloatingPoint(setting):
                widget = TaskSettingFloatingPointWidget(parent=self)
                widget.setRange(setting.minimum(), setting.maximum())
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeInteger(setting):
                widget = TaskSettingIntegerWidget(parent=self)
                widget.setRange(setting.minimum(), setting.maximum())
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeOptionList(setting):
                widget = TaskSettingOptionListWidget(parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeText(setting):
                widget = TaskSettingTextWidget(parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            else:
                raise RuntimeError(f'Unknown setting {setting.name()}')
        return self._taskSettingWidgets
    
    def createLabel(self, setting) -> QLabel:
        displayName = setting.displayName()
        if not setting.optional():
            displayName += '*'
        return QLabel(displayName)
    
    def createButtonsWidget(self) -> None:
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.cancel)
        saveAndCloseSettingsButton = QPushButton('Save and Close Settings')
        saveAndCloseSettingsButton.clicked.connect(self.saveAndCloseSettings)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(cancelButton)
        buttonsLayout.addWidget(saveAndCloseSettingsButton)
        buttonsLayout.setAlignment(Qt.AlignRight)
        buttonsWidget = QWidget()
        buttonsWidget.setLayout(buttonsLayout)
        return buttonsWidget
    
    def cancel(self) -> None:
        self.reject()

    def saveAndCloseSettings(self) -> None:
        pass

    def show(self):
        return self.exec_()