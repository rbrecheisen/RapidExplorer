import os

from PySide6.QtCore import Qt, QSize, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QSizePolicy
from PySide6.QtGui import QAction, QGuiApplication

from data.datamanager import DataManager
from widgets.datadockwidget import DataDockWidget
from widgets.viewersdockwidget import ViewersDockWidget
from widgets.taskdockwidget import TaskDockWidget
from widgets.mainviewerdockwidget import MainViewerDockWidget
from utils import Configuration

WINDOWTITLE = 'Mosamatic Desktop 1.0'
# FILESETPATH = os.path.join(os.getenv('HOME'), 'Desktop', 'downloads', 'dataset', 'scan1')
# FILEPATH = os.path.join(os.getenv('HOME'), 'Desktop', 'downloads', 'dataset', 'scan1', 'image-00000.dcm')


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._settings = Configuration().qSettings()
        self._dataDockWidget = None
        self._tasksDockWidget = None
        self._mainViewDockWidget = None
        # self._viewsDockWidget = None
        self._defaultLayout = None       
        self._dataManager = DataManager()
        self._dataManager.signal().updated.connect(self.dataUpdated) 
        self.initUi()

    # Initialization

    def initUi(self) -> None:
        self.initActionsAndMenus()
        self.initDataDockWidget()
        self.initTaskDockWidget()
        self.initMainViewerDockWidget()
        # self.initViewersDockWidget()
        self.initMainWindow()

    def initActionsAndMenus(self) -> None:
        importFileAction = QAction('Import File...', self)
        importFileSetAction = QAction('Import File Set...', self)
        deleteAllFileSetsAction = QAction('Delete All Data from Database', self)
        resetLayoutAction = QAction('Reset Layout', self)
        showApplicationInfoAction = QAction('Show Application Info...', self)
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
        aboutMenu = QMenu(f'About')
        aboutMenu.addAction(showApplicationInfoAction)
        self.menuBar().addMenu(dataMenu)
        self.menuBar().addMenu(viewMenu)
        self.menuBar().addMenu(aboutMenu)
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

    # def initViewersDockWidget(self) -> None:
    #     self._viewsDockWidget = ViewersDockWidget(title='Views')
    #     self._viewsDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
    #     self.addDockWidget(Qt.RightDockWidgetArea, self._viewsDockWidget)

    def initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dataDockWidget, self._tasksDockWidget, Qt.Vertical)
        # self.splitDockWidget(self._mainViewDockWidget, self._viewsDockWidget, Qt.Vertical)
        self.setWindowTitle(WINDOWTITLE)
        self.setWindowSize()
        self.centerWindow()
        self.saveDefaultLayout()

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

    def saveDefaultLayout(self) -> None:
        self._defaultLayout = self.saveState()

    def resetLayout(self) -> None:
        self.restoreState(self._defaultLayout)

    def setWindowSize(self) -> None:
        size = self._settings.value('mainWindowSize', None)
        if not size:
            size = QSize(970, 760)
            self._settings.setValue('mainWindowSize', size)
        self.resize(size)

    # Exit

    def exitApplication(self) -> None:
        self._settings.setValue('mainWindowSize', self.size())
        QApplication.exit()