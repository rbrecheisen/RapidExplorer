from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

from settings.settings import Settings
from widgets.settingbooleanwidget import SettingBooleanWidget
from widgets.settingfilesetpathwidget import SettingFileSetPathWidget
from widgets.settingfilesetwidget import SettingFileSetWidget
from widgets.settingfloatingpointwidget import SettingFloatingPointWidget
from widgets.settingintegersliderwidget import SettingIntegerSliderWidget
from widgets.settingintegerspinboxwidget import SettingIntegerSpinBoxWidget
from widgets.settinglabelwidget import SettingLabelWidget
from widgets.settingoptionlistwidget import SettingOptionListWidget
from widgets.settingtextwidget import SettingTextWidget


class TaskSettingsDialog(QDialog):
    def __init__(self, taskSettings: Settings) -> None:
        super(TaskSettingsDialog, self).__init__()
        self._taskSettings = taskSettings
        self._taskSettingWidgets = {}
        self.initUi()

    def taskSettings(self) -> Settings:
        return self._taskSettings

    def initUi(self) -> None:
        self._taskSettingWidgets = self.createTaskSettingWidgets()
        layout = QVBoxLayout()
        for name in self._taskSettingWidgets.keys():
            displayLabel = self._taskSettingWidgets[name][1]
            if displayLabel:
                layout.addWidget(displayLabel)
            layout.addWidget(self._taskSettingWidgets[name][0])
        layout.addWidget(self.createButtonsWidget())
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        # self.resize(self.sizeHint())
        self.setFixedWidth(400)
        self.setWindowTitle(self._taskSettings.name())


    def createTaskSettingWidgets(self) ->None:
        settings = self._taskSettings
        for setting in settings.all():
            if settings.isTypeBoolean(setting) and setting.visible():
                widget = SettingBooleanWidget(setting=setting, parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFileSetPath(setting) and setting.visible():
                widget = SettingFileSetPathWidget(setting=setting, parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFileSet(setting) and setting.visible():
                widget = SettingFileSetWidget(setting=setting, parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFloatingPoint(setting) and setting.visible():
                widget = SettingFloatingPointWidget(setting=setting, parent=self)
                widget.setRange(setting.minimum(), setting.maximum())
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeInteger(setting) and setting.visible():
                if setting.isWidgetTypeSpinBox():
                    widget = SettingIntegerSpinBoxWidget(setting=setting, parent=self)
                else:
                    widget = SettingIntegerSliderWidget(setting=setting, parent=self)
                    widget.setSingleStep(setting.step())
                widget.setRange(setting.minimum(), setting.maximum())
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeLabel(setting) and setting.visible():
                widget = SettingLabelWidget(setting=setting, parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, None)

            elif settings.isTypeOptionList(setting) and setting.visible():
                widget = SettingOptionListWidget(setting=setting, parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeText(setting) and setting.visible():
                widget = SettingTextWidget(setting=setting, parent=self)
                self._taskSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            else:
                pass
        return self._taskSettingWidgets
    
    def createLabel(self, setting) -> QLabel:
        displayName = setting.displayName()
        if not setting.optional():
            displayName += ' *'
        return QLabel(displayName)
    
    def createButtonsWidget(self) -> None:
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.cancel)
        saveAndCloseSettingsButton = QPushButton('Save and Close')
        saveAndCloseSettingsButton.setFocus()
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
        for setting in self.taskSettings().all():
            if not setting.optional():
                if setting.value() is None:
                    QMessageBox.critical(self, 'Error', f'Setting {setting.name()} cannot be empty!')
                    return 
        self.accept()

    def show(self):
        return self.exec_()