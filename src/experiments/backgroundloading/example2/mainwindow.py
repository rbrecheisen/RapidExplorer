import os

from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QProgressDialog, QVBoxLayout,QPushButton)
from PySide6.QtGui import QGuiApplication

from data.filecache import FileCache
from data.dbsession import DbSession
from data.fileimporter import FileImporter
from data.filesetimporter import FileSetImporter
from data.multifilesetimporter import MultiFileSetImporter
from data.multifilesetmodel import MultiFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader
from widgets.registeredmultifilesetmodeltreeview import RegisteredMultiFileSetModelTreeView
from data.dicomfiletype import DicomFileType

MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._progressBarDialog = None
        self._fileImporter = None
        self._fileSetImporter = None
        self._multiFileSetImporter = None
        self._treeView = None
        self._initUi()

    def _initUi(self) -> None:
        importDicomFileButton = QPushButton('Import DICOM Image...')
        importDicomFileSetButton = QPushButton('Import DICOM Image Series..')
        importDicomMultiFileSetButton = QPushButton('Import Multiple DICOM Image Series..')
        printFileCacheButton = QPushButton('Print File Cache')        
        importDicomFileButton.clicked.connect(self._importDicomFile)
        importDicomFileSetButton.clicked.connect(self._importDicomFileSet)
        importDicomMultiFileSetButton.clicked.connect(self._importDicomMultiFileSet)
        printFileCacheButton.clicked.connect(self._printFileCache)      
        self._treeView = RegisteredMultiFileSetModelTreeView()
        layout = QVBoxLayout()
        layout.addWidget(importDicomFileButton)
        layout.addWidget(importDicomFileSetButton)
        layout.addWidget(importDicomMultiFileSetButton)
        layout.addWidget(printFileCacheButton)
        layout.addWidget(self._treeView)
        widget = QWidget()
        widget.setLayout(layout)
        self._progressBarDialog = QProgressDialog('Importing Files...', 'Abort Import', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()
        self.setCentralWidget(widget)
        self.setWindowTitle('RapidExplorer')
        self._centerWindow()

    def _importDicomFile(self):
        self._progressBarDialog.show()
        self._progressBarDialog.setValue(0)
        self._fileImporter = FileImporter(path=FILEPATH, fileType=DicomFileType)
        self._fileImporter.signal().progress.connect(self._fileImporterProgress)
        QThreadPool.globalInstance().start(self._fileImporter)

    def _importDicomFileSet(self):
        self._progressBarDialog.show()
        self._progressBarDialog.setValue(0)
        self._fileSetImporter = FileSetImporter(path=FILESETPATH, fileType=DicomFileType)
        self._fileSetImporter.signal().progress.connect(self._fileSetImporterProgress)
        QThreadPool.globalInstance().start(self._fileSetImporter)

    def _importDicomMultiFileSet(self):
        self._progressBarDialog.show()
        self._progressBarDialog.setValue(0)
        self._multiFileSetImporter = MultiFileSetImporter(path=MULTIFILESETPATH, fileType=DicomFileType)
        self._multiFileSetImporter.signal().progress.connect(self._multiFileSetImporterProgress)
        QThreadPool.globalInstance().start(self._multiFileSetImporter)

    def _fileImporterProgress(self, progress):
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._treeView.addRegisteredMultiFileSetModel(self._fileImporter.data())

    def _fileSetImporterProgress(self, progress):
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._treeView.addRegisteredMultiFileSetModel(self._fileSetImporter.data())

    def _multiFileSetImporterProgress(self, progress):
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._treeView.addRegisteredMultiFileSetModel(self._multiFileSetImporter.data())

    def _printFileCache(self):
        FileCache().printFiles()

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))