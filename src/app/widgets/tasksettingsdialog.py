from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

from tasks.task import Task
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
        layout = QVBoxLayout()
        for name in self._taskSettingWidgets.keys():
            layout.addWidget(self._taskSettingWidgets[name][1])   # First widget display label
            layout.addWidget(self._taskSettingWidgets[name][0])   # Then widget
        layout.addWidget(self.createButtonsWidget())
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.resize(self.sizeHint())


    def createTaskSettingWidgets(self) ->None:
        settings = self._task.settings()
        for setting in settings.all():
            if settings.isTypeBoolean(setting) and setting.visible():
                widget = TaskSettingBooleanWidget(parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFileSet(setting) and setting.visible():
                widget = TaskSettingFileSetWidget(parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFloatingPoint(setting) and setting.visible():
                widget = TaskSettingFloatingPointWidget(parent=self)
                widget.setRange(setting.minimum(), setting.maximum())
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeInteger(setting) and setting.visible():
                widget = TaskSettingIntegerWidget(parent=self)
                widget.setRange(setting.minimum(), setting.maximum())
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeOptionList(setting) and setting.visible():
                widget = TaskSettingOptionListWidget(parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeText(setting) and setting.visible():
                widget = TaskSettingTextWidget(parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            else:
                print(f'Unknown or invisible setting {setting.name()}')
        return self._taskSettingWidgets
    
    def createLabel(self, setting) -> QLabel:
        displayName = setting.displayName()
        if not setting.optional():
            displayName += ' *'
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
        raise RuntimeWarning('Implement this!')

    def show(self):
        return self.exec_()