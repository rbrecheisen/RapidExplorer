import os

from PySide6.QtCore import Qt, QSize, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressDialog, QMessageBox
from PySide6.QtGui import QAction, QGuiApplication

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
WINDOWTITLE = 'Mosamatic 2.0'


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
        self._defaultLayout = None        
        self.initUi()

    def initUi(self) -> None:
        self.initActionsAndMenus()
        self.initDataDockWidget()
        self.initTaskDockWidget()
        self.initMainViewDockWidget()
        self.initViewDockWidget()
        self.initProgressBarDialog()
        self.initMainWindow()

    def initActionsAndMenus(self) -> None:
        importFileAction = QAction('Import File...', self)
        importFileSetAction = QAction('Import File Set...', self)
        deleteAllFileSetsAction = QAction('Delete All Data from Database', self)
        resetLayoutAction = QAction('Reset Layout', self)
        exitApplicationAction = QAction('Exit', self)
        importFileAction.triggered.connect(self.importFile)
        importFileSetAction.triggered.connect(self.importFileSet)
        deleteAllFileSetsAction.triggered.connect(self.deleteAllFileSets)
        resetLayoutAction.triggered.connect(self.resetLayout)
        exitApplicationAction.triggered.connect(self.exitApplication)
        dataMenu = QMenu('Data')
        dataMenu.addAction(importFileAction)
        dataMenu.addAction(importFileSetAction)
        dataMenu.addSeparator()
        dataMenu.addAction(deleteAllFileSetsAction)
        dataMenu.addSeparator()
        dataMenu.addAction(exitApplicationAction)
        viewMenu = QMenu('View')
        viewMenu.addAction(resetLayoutAction)
        self.menuBar().addMenu(dataMenu)
        self.menuBar().addMenu(viewMenu)
        self.menuBar().setNativeMenuBar(False)

    def initDataDockWidget(self) -> None:
        self._dataDockWidget = DataDockWidget('Data')
        self._dataDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dataDockWidget)

    def initTaskDockWidget(self) -> None:
        self._tasksDockWidget = TaskDockWidget('Tasks')
        self._tasksDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._tasksDockWidget)

    def initMainViewDockWidget(self) -> None:
        self._mainViewDockWidget = MainViewDockWidget('Main View')
        self._mainViewDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._mainViewDockWidget)

    def initViewDockWidget(self) -> None:
        self._viewsDockWidget = ViewsDockWidget('Views')
        self._viewsDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._viewsDockWidget)

    def initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Importing Files...', 'Abort Import', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

    def initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dataDockWidget, self._tasksDockWidget, Qt.Vertical)
        self.splitDockWidget(self._mainViewDockWidget, self._viewsDockWidget, Qt.Vertical)
        self.setWindowTitle(WINDOWTITLE)
        self.setWindowSize()
        self.centerWindow()
        self.saveDefaultLayout()

    def importFile(self) -> None:
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open File', FILEPATH)
        if filePath:
            pass

    def importFileSet(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open File Set', FILESETPATH)
        if dirPath:
            pass

    def deleteAllFileSets(self) -> None:
        self._dataManager.deleteAllFileSets()

    def resetLayout(self) -> None:
        self.restoreState(self._defaultLayout)

    def exitApplication(self) -> None:
        self._settings.setValue('mainWindowSize', self.size())
        QApplication.exit()

    # def _importDicomFile(self) -> None:
    #     filePath, _ = QFileDialog.getOpenFileName(self, 'Open DICOM Image', FILEPATH)
    #     if filePath:
    #         self._progressBarDialog.show()
    #         self._progressBarDialog.setValue(0)
    #         self._dataManager.signal().progress.connect(self._dataManagerFileImportProgress)
    #         self._dataManager.importFile(filePath=filePath, fileType=DicomFileType())

    # def _importDicomFileSet(self) -> None:
    #     dirPath = QFileDialog.getExistingDirectory(self, 'Open DICOM Image Series', FILESETPATH)
    #     if dirPath:
    #         self._progressBarDialog.show()
    #         self._progressBarDialog.setValue(0)
    #         self._dataManager.signal().progress.connect(self._dataManagerFileSetImportProgress)
    #         self._dataManager.importFileSet(dirPath=dirPath, fileType=DicomFileType())

    # def _importDicomMultiFileSet(self) -> None:
    #     dirPath = QFileDialog.getExistingDirectory(self, 'Open Multiple DICOM Image Series', MULTIFILESETPATH)
    #     if dirPath:            
    #         self._progressBarDialog.show()
    #         self._progressBarDialog.setValue(0)
    #         self._dataManager.signal().progress.connect(self._dataManagerMultiFileSetImportProgress)
    #         self._dataManager.importMultiFileSet(dirPath=dirPath, fileType=DicomFileType())

    # def _importL3FileSet(self) -> None:
    #     dirPath = QFileDialog.getExistingDirectory(self, 'Open DICOM Image Series', FILESETPATH)
    #     if dirPath:
    #         self._progressBarDialog.show()
    #         self._progressBarDialog.setValue(0)
    #         self._dataManager.signal().progress.connect(self._dataManagerFileSetImportProgress)
    #         self._dataManager.importFileSet(dirPath=dirPath, fileType=DicomFileType())

    # def _importTensorFlowModelFileSet(self) -> None:
    #     dirPath = QFileDialog.getExistingDirectory(self, 'Open DICOM Image Series', FILESETPATH)
    #     if dirPath:
    #         self._progressBarDialog.show()
    #         self._progressBarDialog.setValue(0)
    #         self._dataManager.signal().progress.connect(self._dataManagerFileSetImportProgress)
    #         self._dataManager.importFileSet(dirPath=dirPath, fileType=AllFileType())

    # def _dataManagerFileImportProgress(self, progress) -> None:
    #     self._progressBarDialog.setValue(progress)
    #     if progress == 100:
    #         self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._dataManager.data())
    #         self._dataManager.signal().progress.disconnect(self._dataManagerFileImportProgress)

    # def _dataManagerFileSetImportProgress(self, progress) -> None:
    #     self._progressBarDialog.setValue(progress)            
    #     if progress == 100:
    #         self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._dataManager.data())
    #         self._dataManager.signal().progress.disconnect(self._dataManagerFileSetImportProgress)

    # def _dataManagerMultiFileSetImportProgress(self, progress) -> None:
    #     self._progressBarDialog.setValue(progress)
    #     if progress == 100:
    #         self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._dataManager.data())
    #         self._dataManager.signal().progress.disconnect(self._dataManagerMultiFileSetImportProgress)

    # def _printFileCache(self) -> None:
    #     self._dataManager.printFileCache()

    # def _deleteAllData(self) -> None:
    #     self._dataManager.deleteAllData()
    #     currentPlugin = self._pluginManager.currentPlugin()
    #     if currentPlugin:
    #         if self._pluginManager.isViewerPlugin(currentPlugin):
    #             currentPlugin.clearData()
    #     self._dataDockWidget.clearData()        

    def saveDefaultLayout(self) -> None:
        self._defaultLayout = self.saveState()

    def setWindowSize(self) -> None:
        size = self._settings.value('mainWindowSize', None)
        if not size:
            size = QSize(970, 760)
            self._settings.setValue('mainWindowSize', size)
        self.resize(size)

    def centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))