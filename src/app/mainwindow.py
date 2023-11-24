import os

from PySide6.QtCore import Qt, QSize, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressDialog
from PySide6.QtGui import QAction, QGuiApplication

from plugins.pluginmanager import PluginManager
from data.dicomfiletype import DicomFileType
from data.datamanager import DataManager
from widgets.datadockwidget import DataDockWidget
from widgets.viewdockwidget import ViewsDockWidget
from widgets.taskdockwidget import TaskDockWidget
from widgets.mainviewdockwidget import MainViewDockWidget

MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')
MAINWINDOWSIZE = (1024, 800)
ORGANISATION = 'Rbeesoft'
APPLICATIONNAME = 'RapidExplorer'


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        # self._settings = QSettings(ORGANISATION, APPLICATIONNAME)
        self._dataDockWidget = None
        self._tasksDockWidget = None
        self._viewsDockWidget = None
        self._mainViewDockWidget = None
        self._progressBarDialog = None
        self._databaseManager = DataManager()
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
        self._initViewDockWidget()
        self._initMainViewDockWidget()
        self._initProgressBarDialog()
        self._initMainWindow()

    def _initMenus(self) -> None:
        importDicomFileAction = QAction('Import DICOM Image...', self)
        importDicomFileSetAction = QAction('Import DICOM Image Series...', self)
        importDicomMultiFileSetAction = QAction('Import Multiple DICOM Image Series...', self)
        printFileCacheAction = QAction('Print File Cache', self)
        deleteAllDataAction = QAction('Delete All Data from Database', self)
        resetLayoutAction = QAction('Reset Layout', self)
        exitAction = QAction('Exit', self)
        importDicomFileAction.triggered.connect(self._importDicomFile)
        importDicomFileSetAction.triggered.connect(self._importDicomFileSet)
        importDicomMultiFileSetAction.triggered.connect(self._importDicomMultiFileSet)
        printFileCacheAction.triggered.connect(self._printFileCache)
        deleteAllDataAction.triggered.connect(self._deleteAllData)
        resetLayoutAction.triggered.connect(self._resetLayout)
        exitAction.triggered.connect(self._exit)
        datasetsMenu = QMenu('Data')
        datasetsMenu.addAction(importDicomFileAction)
        datasetsMenu.addAction(importDicomFileSetAction)
        datasetsMenu.addAction(importDicomMultiFileSetAction)
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
        self._dataDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dataDockWidget)

    def _initTaskDockWidget(self) -> None:
        self._tasksDockWidget = TaskDockWidget('Tasks')
        self._tasksDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._tasksDockWidget)

    def _initViewDockWidget(self) -> None:
        self._viewsDockWidget = ViewsDockWidget('Views')
        self._viewsDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._viewsDockWidget)

    def _initMainViewDockWidget(self) -> None:
        self._mainViewDockWidget = MainViewDockWidget('Main View')
        self._mainViewDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._mainViewDockWidget)

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
        self.setFixedSize(QSize(MAINWINDOWSIZE[0], MAINWINDOWSIZE[1]))
        self.setWindowTitle('RapidExplorer v1.0')
        self._centerWindow()
        self._defaultLayout = self.saveState()

    def _importDicomFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open DICOM Image', FILEPATH)
        if filePath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._databaseManager.signal().progress.connect(self._databaseManagerFileImportProgress)
            self._databaseManager.importFile(filePath=filePath, fileType=DicomFileType())

    def _importDicomFileSet(self):
        dirPath = QFileDialog.getExistingDirectory(self, 'Open DICOM Image Series', FILESETPATH)
        if dirPath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._databaseManager.signal().progress.connect(self._databaseManagerFileSetImportProgress)
            self._databaseManager.importFileSet(dirPath=dirPath, fileType=DicomFileType())

    def _importDicomMultiFileSet(self):
        dirPath = QFileDialog.getExistingDirectory(self, 'Open Multiple DICOM Image Series', MULTIFILESETPATH)
        if dirPath:            
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._databaseManager.signal().progress.connect(self._databaseManagerMultiFileSetImportProgress)
            self._databaseManager.importMultiFileSet(dirPath=dirPath, fileType=DicomFileType())

    def _databaseManagerFileImportProgress(self, progress):
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._databaseManager.data())
            self._databaseManager.signal().progress.disconnect(self._databaseManagerFileImportProgress)

    def _databaseManagerFileSetImportProgress(self, progress):
        self._progressBarDialog.setValue(progress)            
        if progress == 100:
            self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._databaseManager.data())
            self._databaseManager.signal().progress.disconnect(self._databaseManagerFileSetImportProgress)

    def _databaseManagerMultiFileSetImportProgress(self, progress):
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._databaseManager.data())
            self._databaseManager.signal().progress.disconnect(self._databaseManagerMultiFileSetImportProgress)

    def _printFileCache(self):
        self._databaseManager.printFileCache()

    def _deleteAllData(self):
        self._databaseManager.deleteAllData()
        currentPlugin = self._pluginManager.currentPlugin()
        if currentPlugin:
            if self._pluginManager.isViewPlugin(currentPlugin):
                currentPlugin.clearData()
        self._dataDockWidget.clearData()        

    def _resetLayout(self):
        self.restoreState(self._defaultLayout)

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))

    def _exit(self) -> None:
        QApplication.exit()