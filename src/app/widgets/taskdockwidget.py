from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton

from widgets.dockwidget import DockWidget
from plugins.pluginmanager import PluginManager


class TaskDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(TaskDockWidget, self).__init__(title)
        self._comboBoxTaskPlugins = None
        self._runTaskButton = None
        self._initUi()
        self._loadTaskPlugins()

    def _initUi(self) -> None:
        self._comboBoxTaskPlugins = QComboBox(self)
        self._comboBoxTaskPlugins.currentIndexChanged.connect(self._currentIndexChanged)
        showSettingsDialogButton = QPushButton('Edit Settings...')
        showSettingsDialogButton.setFixedWidth(200)
        showSettingsDialogButton.clicked.connect(self._showSettingsDialog)
        self._runTaskButton = QPushButton('Run task')
        self._runTaskButton.clicked.connect(self._runTask)
        # self._runTaskButton.setEnabled(False)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(showSettingsDialogButton)
        buttonLayout.addWidget(self._runTaskButton)
        buttonLayout.setAlignment(Qt.AlignRight)
        buttonWidget = QWidget()
        buttonWidget.setLayout(buttonLayout)
        layout = QVBoxLayout()
        layout.addWidget(self._comboBoxTaskPlugins)
        layout.addWidget(buttonWidget)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)    
        self.setWidget(widget)
        self.setMinimumHeight(200)

    def _currentIndexChanged(self, index) -> None:
        selectedText = self._comboBoxTaskPlugins.itemText(index)
        manager = PluginManager()        
        plugin = manager.taskPlugin(selectedText)
        if plugin:
            manager.setCurrentTaskPlugin(plugin)

    def _showSettingsDialog(self) -> None:
        selectedText = self._comboBoxTaskPlugins.currentText()
        if selectedText:
            manager = PluginManager()
            plugin = manager.taskPlugin(selectedText)
            plugin.showSettingsDialog()

    def _runTask(self) -> None:
        selectedText = self._comboBoxTaskPlugins.currentText()
        if selectedText:
            manager = PluginManager()
            plugin = manager.taskPlugin(selectedText)
            plugin.run()


    def _loadTaskPlugins(self) -> None:
        self._comboBoxTaskPlugins.clear()
        self._comboBoxTaskPlugins.addItem(None)
        manager = PluginManager()
        for pluginName in manager.taskPlugins().keys():
            self._comboBoxTaskPlugins.addItem(pluginName)
