import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressBar
from PySide6.QtGui import QAction, QGuiApplication

from mosamaticdesktop.data.datamanager import DataManager
from mosamaticdesktop.widgets.datadockwidget import DataDockWidget
from mosamaticdesktop.widgets.taskdockwidget import TaskDockWidget
from mosamaticdesktop.widgets.mainviewerdockwidget import MainViewerDockWidget
from mosamaticdesktop.utils import Configuration

WINDOWTITLE = 'Mosamatic Desktop 1.0'
FILESETPATH = os.path.join(os.getenv('HOME'), 'Desktop', 'downloads', 'dataset', 'scan1')
FILEPATH = os.path.join(os.getenv('HOME'), 'Desktop', 'downloads', 'dataset', 'scan1', 'image-00000.dcm')


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._settings = Configuration().qSettings()
        self._dataDockWidget = None
        self._tasksDockWidget = None
        self._mainViewDockWidget = None
        self._defaultLayout = None       
        self._progressBar = None
        self._dataManager = DataManager()
        self._dataManager.signal().updated.connect(self.dataUpdated) 
        self.initUi()

    # Initialization

    def initUi(self) -> None:
        self.initActionsAndMenus()
        self.initProgressBar()
        self.initDataDockWidget()
        self.initTaskDockWidget()
        self.initMainViewerDockWidget()
        self.initMainWindow()

    def initActionsAndMenus(self) -> None:
        importFileAction = QAction('Import File...', self)
        importFileSetAction = QAction('Import File Set...', self)
        deleteAllFileSetsAction = QAction('Delete All Data from Database', self)
        showApplicationInfoAction = QAction('Show Application Info...', self)
        exitApplicationAction = QAction('Exit', self)
        importFileAction.triggered.connect(self.importFile)
        importFileSetAction.triggered.connect(self.importFileSet)
        deleteAllFileSetsAction.triggered.connect(self.deleteAllFileSets)
        exitApplicationAction.triggered.connect(self.exitApplication)
        dataMenu = QMenu('Data')
        dataMenu.addAction(importFileAction)
        dataMenu.addAction(importFileSetAction)
        dataMenu.addSeparator()
        dataMenu.addAction(deleteAllFileSetsAction)
        dataMenu.addSeparator()
        dataMenu.addAction(exitApplicationAction)
        aboutMenu = QMenu(f'About')
        aboutMenu.addAction(showApplicationInfoAction)
        self.menuBar().addMenu(dataMenu)
        self.menuBar().addMenu(aboutMenu)
        self.menuBar().setNativeMenuBar(False)

    def initProgressBar(self) -> None:
        self._progressBar = QProgressBar(self)
        self._progressBar.setRange(0, 100)
        self._progressBar.setValue(0)
        self.statusBar().addPermanentWidget(self._progressBar)

    def initDataDockWidget(self) -> None:
        self._dataDockWidget = DataDockWidget(title='Data')
        self._dataDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dataDockWidget)

    def initTaskDockWidget(self) -> None:
        self._tasksDockWidget = TaskDockWidget(title='Tasks', progressBar=self._progressBar)
        self._tasksDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.BottomDockWidgetArea)
        self._tasksDockWidget.setFixedHeight(200)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._tasksDockWidget)

    def initMainViewerDockWidget(self) -> None:
        self._mainViewDockWidget = MainViewerDockWidget(title='Main View', progressBar=self._progressBar)
        self._mainViewDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._mainViewDockWidget)

    def initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dataDockWidget, self._tasksDockWidget, Qt.Vertical)
        self.setWindowTitle(WINDOWTITLE)
        self.centerWindow()
        self.restoreGeometry(self._settings.value('windowGeometry'))
        self.restoreState(self._settings.value('windowState'))

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
            fs = self._dataManager.createFileSet(fileSetPath=fileSetPath)

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

    # Exit
        
    def exitApplication(self) -> None:
        self._settings.setValue('windowGeometry', self.saveGeometry())
        self._settings.setValue('windowState', self.saveState())
        QApplication.exit()