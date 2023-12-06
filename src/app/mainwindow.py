import os
import sys

from PySide6.QtCore import Qt, QSize, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressDialog, QMessageBox
from PySide6.QtGui import QAction, QGuiApplication

from logger import Logger
# from settingsinifile import SettingsIniFile
from commitid import CommitId
from data.datamanager import DataManager
from data.fileset import FileSet
from widgets.datadockwidget import DataDockWidget
from widgets.viewersdockwidget import ViewersDockWidget
from widgets.taskdockwidget import TaskDockWidget
from widgets.mainviewerdockwidget import MainViewerDockWidget
from widgets.filetypedialog import FileTypeDialog

# SETTINGSPATH = os.environ.get('SETTINGSPATH', 'settings.ini')
# SETTINGSPATH = 'settings.ini'
# if not os.path.isfile(SETTINGSPATH):
#     SETTINGSPATH = os.path.join(os.path.dirname(sys.executable), 'settings.ini')

# GITCOMMITID = os.environ.get('GITCOMMITID', open('gitcommitid.txt', 'r').readline().strip())
# GITCOMMITIDPATH = 'gitcommitid.txt'
# if not os.path.isfile(GITCOMMITIDPATH):
#     GITCOMMITIDPATH = os.path.join(os.path.dirname(sys.executable), 'gitcommitid.txt')
# GITCOMMITID = open(GITCOMMITIDPATH, 'r').readline().strip()

MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')
ORGANISATION = 'Rbeesoft'
APPLICATIONNAME = 'RapidExplorer'
WINDOWTITLE = 'Mosamatic Desktop 1.0'

LOGGER = Logger()
LOGGER.info(f'WINDOWTITLE: {WINDOWTITLE}')


class MainWindow(QMainWindow):
    def __init__(self, settingsPath: str) -> None:
        super(MainWindow, self).__init__()
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
        self.initMainViewerDockWidget()
        self.initViewersDockWidget()
        self.initProgressBarDialog()
        self.initMainWindow()

    def initActionsAndMenus(self) -> None:
        importFileAction = QAction('Import File...', self)
        importFileSetAction = QAction('Import File Set...', self)
        importFileSetWithFileTypeAction = QAction('Import File Set with File Type...', self)
        deleteAllFileSetsAction = QAction('Delete All Data from Database', self)
        resetLayoutAction = QAction('Reset Layout', self)
        showApplicationInfoAction = QAction('Show Application Info...', self)
        exitApplicationAction = QAction('Exit', self)
        importFileAction.triggered.connect(self.importFile)
        importFileSetAction.triggered.connect(self.importFileSet)
        importFileSetWithFileTypeAction.triggered.connect(self.importFileSetWithFileType)
        deleteAllFileSetsAction.triggered.connect(self.deleteAllFileSets)
        resetLayoutAction.triggered.connect(self.resetLayout)
        showApplicationInfoAction.triggered.connect(self.showApplicationInfo)
        exitApplicationAction.triggered.connect(self.exitApplication)
        dataMenu = QMenu('Data')
        dataMenu.addAction(importFileAction)
        dataMenu.addAction(importFileSetAction)
        dataMenu.addAction(importFileSetWithFileTypeAction)
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
        self._tasksDockWidget.signal().finished.connect(self.taskFinished)
        self._tasksDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._tasksDockWidget)

    def initMainViewerDockWidget(self) -> None:
        self._mainViewDockWidget = MainViewerDockWidget(title='Main View')
        self._mainViewDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._mainViewDockWidget)

    def initViewersDockWidget(self) -> None:
        self._viewsDockWidget = ViewersDockWidget(title='Views')
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

    # QAction handlers

    def importFile(self) -> None:
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open File', FILEPATH)
        if filePath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dataManager.signal().progress.connect(self.fileImportProgress)
            self._dataManager.signal().finished.connect(self.fileImportFinished)
            self._dataManager.importFile(filePath=filePath)

    def importFileSet(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open File Set', FILESETPATH)
        if dirPath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dataManager.signal().progress.connect(self.fileSetImportProgress)
            self._dataManager.signal().finished.connect(self.fileSetImportFinished)
            self._dataManager.importFileSet(fileSetPath=dirPath)

    def importFileSetWithFileType(self) -> None:
        fileTypeDialog = FileTypeDialog(self)
        resultCode = fileTypeDialog.show()
        if resultCode == FileTypeDialog.Accepted:
            fileType = fileTypeDialog.selectedFileType()
            recursive = fileTypeDialog.recursive()
            dirPath = QFileDialog.getExistingDirectory(self, 'Open File Set', FILESETPATH)
            if dirPath:
                self._progressBarDialog.show()
                self._progressBarDialog.setValue(0)
                self._dataManager.signal().progress.connect(self.fileSetImportProgress)
                self._dataManager.signal().finished.connect(self.fileSetImportFinished)
                self._dataManager.importFileSet(fileSetPath=dirPath, fileType=fileType, recursive=recursive)

    def deleteAllFileSets(self) -> None:
        self._dataManager.deleteAllFileSets()
        self._dataDockWidget.clearFileSets()
        # Clear current viewer

    def resetLayout(self) -> None:
        self.restoreState(self._defaultLayout)

    def showApplicationInfo(self) -> None:
        commitId = CommitId()
        QMessageBox.information(self, 'Application Information', f'Git Commit ID: {commitId.value()}')

    def exitApplication(self) -> None:
        self._settings.setValue('mainWindowSize', self.size())
        QApplication.exit()

    # Progress handlers

    def fileImportProgress(self, progress) -> None:
        self._progressBarDialog.setValue(progress)
        
    def fileImportFinished(self, fileSet: FileSet) -> None:
        self._dataManager.signal().progress.disconnect(self.fileImportProgress)
        self._dataManager.signal().finished.disconnect(self.fileImportFinished)
        if fileSet is None:
            self._progressBarDialog.close()
            QMessageBox.critical(self, 'Warning', 'File Set Is Empty!')
            return
        self._dataDockWidget.addFileSet(fileSet=fileSet)

    def fileSetImportProgress(self, progress) -> None:
        self._progressBarDialog.setValue(progress)

    def fileSetImportFinished(self, fileSet: FileSet) -> None:
        self._dataManager.signal().progress.disconnect(self.fileSetImportProgress)
        self._dataManager.signal().finished.disconnect(self.fileSetImportFinished)
        if fileSet is None:
            self._progressBarDialog.close()
            QMessageBox.critical(self, 'Warning', 'File Set Is Empty!')
            return
        self._dataDockWidget.addFileSet(fileSet=fileSet)

    def taskFinished(self, outputFileSet: FileSet) -> None:
        self._dataDockWidget.addFileSet(fileSet=outputFileSet)

    # Miscellaneous

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