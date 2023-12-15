from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox

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
from widgets.viewersettingsdialogsignal import ViewerSettingsDialogSignal


class ViewerSettingsDialog(QDialog):
    def __init__(self, viewerSettings: Settings) -> None:
        super(ViewerSettingsDialog, self).__init__()
        self._viewerSettings = viewerSettings
        self._viewerSettingWidgets = {}
        self._interactive = False
        self._interactiveCheckBox = QCheckBox()
        self._interactiveCheckBox.setText('Interactive')
        self._interactiveCheckBox.stateChanged.connect(self.enableInteractive)
        self._signal = ViewerSettingsDialogSignal()
        self.initUi()

    def viewerSettings(self) -> Settings:
        return self._viewerSettings

    def initUi(self) -> None:
        self._viewerSettingWidgets = self.createViewerSettingWidgets()
        layout = QVBoxLayout()
        layout.addWidget(self._interactiveCheckBox)
        for name in self._viewerSettingWidgets.keys():
            displayLabel = self._viewerSettingWidgets[name][1]
            if displayLabel:
                layout.addWidget(displayLabel)
            widget = self._viewerSettingWidgets[name][0]
            layout.addWidget(widget)
        layout.addWidget(self.createButtonsWidget())
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        # self.resize(self.sizeHint())
        self.setFixedWidth(400)
        self.setWindowTitle(self._viewerSettings.name())

    def signal(self) -> ViewerSettingsDialogSignal:
        return self._signal

    def createViewerSettingWidgets(self) ->None:
        settings = self._viewerSettings
        for setting in settings.all():
            if settings.isTypeBoolean(setting) and setting.visible():
                widget = SettingBooleanWidget(setting=setting, parent=self)
                widget.stateChanged.connect(self.settingsUpdated)
                self._viewerSettingWidgets[setting.name()] = (widget, None)

            elif settings.isTypeFileSetPath(setting) and setting.visible():
                widget = SettingFileSetPathWidget(setting=setting, parent=self)
                widget.textChanged.connect(self.settingsUpdated)
                self._viewerSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFileSet(setting) and setting.visible():
                widget = SettingFileSetWidget(setting=setting, parent=self)
                widget.currentIndexChanged.connect(self.settingsUpdated)
                self._viewerSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeFloatingPoint(setting) and setting.visible():
                widget = SettingFloatingPointWidget(setting=setting, parent=self)
                widget.setRange(setting.minimum(), setting.maximum())
                widget.valueChanged.connect(self.settingsUpdated)
                self._viewerSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeInteger(setting) and setting.visible():
                if setting.isWidgetTypeSpinBox():
                    widget = SettingIntegerSpinBoxWidget(setting=setting, parent=self)
                else:
                    widget = SettingIntegerSliderWidget(setting=setting, parent=self)
                    widget.setSingleStep(setting.step())
                widget.setRange(setting.minimum(), setting.maximum())
                widget.valueChanged.connect(self.settingsUpdated)
                self._viewerSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeLabel(setting) and setting.visible():
                widget = SettingLabelWidget(setting=setting, parent=self)
                self._viewerSettingWidgets[setting.name()] = (widget, None)

            elif settings.isTypeOptionList(setting) and setting.visible():
                widget = SettingOptionListWidget(setting=setting, parent=self)
                widget.currentIndexChanged.connect(self.settingsUpdated)
                self._viewerSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            elif settings.isTypeText(setting) and setting.visible():
                widget = SettingTextWidget(setting=setting, parent=self)
                widget.textChanged.connect(self.settingsUpdated)
                self._viewerSettingWidgets[setting.name()] = (widget, self.createLabel(setting=setting))

            else:
                pass
        return self._viewerSettingWidgets
    
    def createLabel(self, setting) -> QLabel:
        displayName = setting.displayName()
        if not setting.optional():
            displayName += ' *'
        return QLabel(displayName)
    
    def createButtonsWidget(self) -> QWidget:
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
    
    def enableInteractive(self, state) -> None:
        self._interactive = not self._interactive

    def settingsUpdated(self, *args) -> None:
        if self._interactive:
            self._signal.updated.emit(True)
    
    def cancel(self) -> None:
        self.reject()

    def saveAndCloseSettings(self) -> None:
        for setting in self.viewerSettings().all():
            if not setting.optional():
                if setting.value() is None:
                    QMessageBox.critical(self, 'Error', f'Setting {setting.name()} cannot be empty!')
                    return 
        self.accept()

    def show(self):
        return self.exec_()