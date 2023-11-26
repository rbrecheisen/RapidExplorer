import os

from PySide6.QtCore import Qt, QSize, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressDialog, QMessageBox
from PySide6.QtGui import QAction, QGuiApplication

import data.engine

from plugins.pluginmanager import PluginManager
from data.dicomfiletype import DicomFileType
from data.allfiletype import AllFileType
from data.datamanager import DataManager
from widgets.datadockwidget import DataDockWidget
from widgets.viewdockwidget import ViewsDockWidget
from widgets.taskdockwidget import TaskDockWidget
from widgets.mainviewdockwidget import MainViewDockWidget

SETTINGSPATH = 'settings.ini'
MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')
MAINWINDOWSIZE = (1024, 800)
ORGANISATION = 'Rbeesoft'
APPLICATIONNAME = 'RapidExplorer'


class MainWindow(QMainWindow):
    def __init__(self, settingsPath: str) -> None:
        super(MainWindow, self).__init__()
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        self._settings = QSettings(settingsPath, QSettings.Format.IniFormat)
        self._dataDockWidget = None
        self._tasksDockWidget = None
        self._mainViewDockWidget = None
        self._viewsDockWidget = None
        self._progressBarDialog = None
        self._dataManager = DataManager()
        self._pluginManager = PluginManager()
        self._fileImporter = None
        self._fileSetImporter = None
        self._multiFileSetImporter = None
        self._defaultLayout = None        
        self._loadPlugins()
        self._initUi()

    def _loadPlugins(self) -> None:
        self._pluginManager.loadAll()

    def _initUi(self) -> None:
        self._initMenus()
        self._initDataDockWidget()
        self._initTaskDockWidget()
        self._initMainViewDockWidget()
        self._initViewDockWidget()
        self._initProgressBarDialog()
        self._initMainWindow()

    def _initMenus(self) -> None:
        # TODO: Make this language-independent using QSettings or another singleton object
        importDicomFileAction = QAction('Import DICOM Image...', self)
        importDicomFileSetAction = QAction('Import DICOM Image Series...', self)
        importDicomMultiFileSetAction = QAction('Import Multiple DICOM Image Series...', self)
        importL3FileSetAction = QAction('Import L3s...', self)
        importTensorFlowModelFileSetAction = QAction('Import TensorFlow Model Files...', self)
        printFileCacheAction = QAction('Print File Cache', self)
        deleteAllDataAction = QAction('Delete All Data from Database', self)
        resetLayoutAction = QAction('Reset Layout', self)
        exitAction = QAction('Exit', self)
        importDicomFileAction.triggered.connect(self._importDicomFile)
        importDicomFileSetAction.triggered.connect(self._importDicomFileSet)
        importDicomMultiFileSetAction.triggered.connect(self._importDicomMultiFileSet)
        importL3FileSetAction.triggered.connect(self._importL3FileSet)
        importTensorFlowModelFileSetAction.triggered.connect(self._importTensorFlowModelFileSet)
        printFileCacheAction.triggered.connect(self._printFileCache)
        deleteAllDataAction.triggered.connect(self._deleteAllData)
        resetLayoutAction.triggered.connect(self._resetToDefaultLayout)
        exitAction.triggered.connect(self._exit)
        datasetsMenu = QMenu('Data')
        datasetsMenu.addAction(importDicomFileAction)
        datasetsMenu.addAction(importDicomFileSetAction)
        datasetsMenu.addAction(importDicomMultiFileSetAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(importL3FileSetAction)
        datasetsMenu.addAction(importTensorFlowModelFileSetAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(printFileCacheAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(deleteAllDataAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(exitAction)
        viewMenu = QMenu('View')
        viewMenu.addAction(resetLayoutAction)
        self.menuBar().addMenu(datasetsMenu)
        self.menuBar().addMenu(viewMenu)
        self.menuBar().setNativeMenuBar(False)

    def _initDataDockWidget(self) -> None:
        self._dataDockWidget = DataDockWidget('Data')
        self._dataDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dataDockWidget)

    def _initTaskDockWidget(self) -> None:
        self._tasksDockWidget = TaskDockWidget('Tasks')
        self._tasksDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._tasksDockWidget)

    def _initMainViewDockWidget(self) -> None:
        self._mainViewDockWidget = MainViewDockWidget('Main View')
        self._mainViewDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._mainViewDockWidget)

    def _initViewDockWidget(self) -> None:
        self._viewsDockWidget = ViewsDockWidget('Views')
        self._viewsDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._viewsDockWidget)

    def _initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Importing Files...', 'Abort Import', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

    def _initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dataDockWidget, self._tasksDockWidget, Qt.Vertical)
        self.splitDockWidget(self._mainViewDockWidget, self._viewsDockWidget, Qt.Vertical)
        self.setWindowTitle('Mosamatic 2.0')  # QSettings!
        self._setSize()
        self._centerWindow()
        self._saveDefaultLayout()

    def _importDicomFile(self) -> None:
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open DICOM Image', FILEPATH)
        if filePath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dataManager.signal().progress.connect(self._dataManagerFileImportProgress)
            self._dataManager.importFile(filePath=filePath, fileType=DicomFileType())

    def _importDicomFileSet(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open DICOM Image Series', FILESETPATH)
        if dirPath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dataManager.signal().progress.connect(self._dataManagerFileSetImportProgress)
            self._dataManager.importFileSet(dirPath=dirPath, fileType=DicomFileType())

    def _importDicomMultiFileSet(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open Multiple DICOM Image Series', MULTIFILESETPATH)
        if dirPath:            
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dataManager.signal().progress.connect(self._dataManagerMultiFileSetImportProgress)
            self._dataManager.importMultiFileSet(dirPath=dirPath, fileType=DicomFileType())

    def _importL3FileSet(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open DICOM Image Series', FILESETPATH)
        if dirPath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dataManager.signal().progress.connect(self._dataManagerFileSetImportProgress)
            self._dataManager.importFileSet(dirPath=dirPath, fileType=DicomFileType())

    def _importTensorFlowModelFileSet(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open DICOM Image Series', FILESETPATH)
        if dirPath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dataManager.signal().progress.connect(self._dataManagerFileSetImportProgress)
            self._dataManager.importFileSet(dirPath=dirPath, fileType=AllFileType())

    def _dataManagerFileImportProgress(self, progress) -> None:
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._dataManager.data())
            self._dataManager.signal().progress.disconnect(self._dataManagerFileImportProgress)

    def _dataManagerFileSetImportProgress(self, progress) -> None:
        self._progressBarDialog.setValue(progress)            
        if progress == 100:
            self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._dataManager.data())
            self._dataManager.signal().progress.disconnect(self._dataManagerFileSetImportProgress)

    def _dataManagerMultiFileSetImportProgress(self, progress) -> None:
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._dataManager.data())
            self._dataManager.signal().progress.disconnect(self._dataManagerMultiFileSetImportProgress)

    def _printFileCache(self) -> None:
        self._dataManager.printFileCache()

    def _deleteAllData(self) -> None:
        self._dataManager.deleteAllData()
        currentPlugin = self._pluginManager.currentPlugin()
        if currentPlugin:
            if self._pluginManager.isViewerPlugin(currentPlugin):
                currentPlugin.clearData()
        self._dataDockWidget.clearData()        

    def _saveDefaultLayout(self) -> None:
        self._defaultLayout = self.saveState()

    def _resetToDefaultLayout(self) -> None:
        self.restoreState(self._defaultLayout)

    def _setSize(self) -> None:
        size = self._settings.value('mainWindowSize', None)
        if not size:
            size = QSize(970, 760)
            self._settings.setValue('mainWindowSize', size)
        self.resize(size)

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))

    def _exit(self) -> None:
        self._settings.setValue('mainWindowSize', self.size())
        QApplication.exit()