import os

from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressBar, QStatusBar, QMessageBox
from PySide6.QtGui import QAction, QGuiApplication

from mosamaticdesktop.data.datamanager import DataManager
from mosamaticdesktop.widgets.datadockwidget import DataDockWidget
from mosamaticdesktop.widgets.taskdockwidget import TaskDockWidget
from mosamaticdesktop.widgets.mainviewerdockwidget import MainViewerDockWidget
from mosamaticdesktop.utils import Configuration
from mosamaticdesktop.logger import Logger

LOGGER = Logger()

WINDOWTITLE = 'Mosamatic Desktop'
# FILESETPATH = os.path.join(os.getenv('HOME'), 'Desktop', 'downloads', 'dataset', 'scan1')
# FILEPATH = os.path.join(os.getenv('HOME'), 'Desktop', 'downloads', 'dataset', 'scan1', 'image-00000.dcm')


class MainWindow(QMainWindow):
    class FileSetLoadedSignal(QObject):
        loaded = Signal(bool)

    def __init__(self, version: str, gitHubCommitId: str) -> None:
        super(MainWindow, self).__init__()
        self._version = version
        LOGGER.info(f'Running Mosamatic Desktop {self._version}...')
        self._gitHubCommitId = gitHubCommitId
        self._settings = Configuration().qSettings()
        self._dataDockWidget = None
        self._tasksDockWidget = None
        self._mainViewDockWidget = None
        self._defaultLayout = None       
        self._dataManager = DataManager()
        self._statusBar = None
        self._progress = 0
        self._progressBar = None
        self._fileSetLoadedSignal = self.FileSetLoadedSignal()
        self._dataManager.signal().updated.connect(self.dataUpdated) 
        self.initUi()

    # Initialization

    def initUi(self) -> None:
        self.initActionsAndMenus()
        self.initDataDockWidget()
        self.initTaskDockWidget()
        # self.initMainViewerDockWidget()
        self.initProgressAndStatusBar()
        self.initMainWindow()

    def initActionsAndMenus(self) -> None:
        importFileAction = QAction('Import File...', self)
        importFileSetAction = QAction('Import File Set...', self)
        # importMultipleFileSetsAction = QAction('Import Multiple File Sets...', self)
        deleteAllFileSetsAction = QAction('Delete All Data from Database', self)
        showApplicationInfoAction = QAction('Show Application Info...', self)
        exitApplicationAction = QAction('Exit', self)
        importFileAction.triggered.connect(self.importFile)
        importFileSetAction.triggered.connect(self.importFileSet)
        # importMultipleFileSetsAction.triggered.connect(self.importMultipleFileSets)
        deleteAllFileSetsAction.triggered.connect(self.deleteAllFileSets)
        showApplicationInfoAction.triggered.connect(self.showApplicationInfo)
        exitApplicationAction.triggered.connect(self.exitApplication)
        dataMenu = QMenu('Data')
        dataMenu.addAction(importFileAction)
        dataMenu.addAction(importFileSetAction)
        # dataMenu.addAction(importMultipleFileSetsAction)
        dataMenu.addSeparator()
        dataMenu.addAction(deleteAllFileSetsAction)
        dataMenu.addSeparator()
        dataMenu.addAction(exitApplicationAction)
        # aboutMenu = QMenu(f'About')
        # aboutMenu.addAction(showApplicationInfoAction)
        self.menuBar().addMenu(dataMenu)
        # self.menuBar().addMenu(aboutMenu)
        self.menuBar().setNativeMenuBar(False)

    def initDataDockWidget(self) -> None:
        self._dataDockWidget = DataDockWidget(title='Data')
        self._dataDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dataDockWidget)

    def initTaskDockWidget(self) -> None:
        self._tasksDockWidget = TaskDockWidget(title='Tasks')
        self._tasksDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.BottomDockWidgetArea)
        self._tasksDockWidget.setFixedHeight(200)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._tasksDockWidget)

    def initMainViewerDockWidget(self) -> None:
        self._mainViewDockWidget = MainViewerDockWidget(title='Main View')
        self._mainViewDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._mainViewDockWidget)

    def initProgressAndStatusBar(self) -> None:
        self._progress = 0
        self._progressBar = QProgressBar(self)
        self._progressBar.setMaximum(100)
        self._progressBar.setMinimum(0)
        self._progressBar.setValue(0)
        self._statusBar = QStatusBar(self)
        self._statusBar.addPermanentWidget(self._progressBar)        

    def initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dataDockWidget, self._tasksDockWidget, Qt.Vertical)
        self.setStatusBar(self._statusBar)
        self.setWindowTitle(f'{WINDOWTITLE} {self._version}')
        self.centerWindow()
        self.restoreGeometry(self._settings.value('windowGeometry'))
        self.restoreState(self._settings.value('windowState'))

    def updateProgressBar(self, step: int, nrSteps: int) -> None:
        self._progress = int(((step + 1) / (nrSteps)) * 100)
        self._progressBar.setValue(self._progress)
        return step + 1

    # Event handlers

    def importFile(self) -> None:
        lastDirectoryOpened = self._settings.value('lastDirectoryOpened')
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open File', lastDirectoryOpened)
        if filePath:
            self._settings.setValue('lastDirectoryOpened', os.path.split(filePath)[0])
            self._dataManager.createFile(filePath=filePath)

    def importFileSet(self) -> None:
        lastDirectoryOpened = self._settings.value('lastDirectoryOpened')
        fileSetPath = QFileDialog.getExistingDirectory(self, 'Open File Set', lastDirectoryOpened)
        if fileSetPath:
            self._settings.setValue('lastDirectoryOpened', fileSetPath)
            self._dataManager.createFileSet(fileSetPath=fileSetPath)

    def importMultipleFileSets(self) -> None:
        lastDirectoryOpened = self._settings.value('lastDirectoryOpened')
        fileSetsRootDirectory = QFileDialog.getExistingDirectory(self, 'Open File Sets Root Directory', lastDirectoryOpened)
        if fileSetsRootDirectory:
            self._settings.setValue('lastDirectoryOpened', fileSetsRootDirectory)
            self._progressBar.setValue(0)
            self._progress = 0
            nrSteps = len(os.listdir(fileSetsRootDirectory))
            step = 0
            for d in os.listdir(fileSetsRootDirectory):
                dPath = os.path.join(fileSetsRootDirectory, d)
                if os.path.isdir(dPath):
                    LOGGER.info(f'Creating fileset from directory {dPath}...')
                    self._dataManager.createFileSet(fileSetPath=dPath)
                    step = self.updateProgressBar(step, nrSteps)

    def deleteAllFileSets(self) -> None:
        self._dataManager.deleteAllFileSets()

    def dataUpdated(self, value) -> None:
        self._dataDockWidget.treeView().loadFileSetsFromDatabase()

    # Layout and positioning

    def centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))

    def showApplicationInfo(self) -> None:
        import torch
        text = f'GPU Enabled: {torch.cuda.is_available()}'
        QMessageBox.information(self, 'Application Info', text)

    # Exit
        
    def exitApplication(self) -> None:
        self._settings.setValue('windowGeometry', self.saveGeometry())
        self._settings.setValue('windowState', self.saveState())
        QApplication.exit()