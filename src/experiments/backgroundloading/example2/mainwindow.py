import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QProgressDialog, QVBoxLayout,QPushButton)
from PySide6.QtGui import QGuiApplication

from data.fileregistrar import FileRegistrar
from data.filesetregistrar import FileSetRegistrar
from data.multifilesetregistrar import MultiFileSetRegistrar
from data.registeredmodelprinter import RegisteredModelPrinter
from data.filecache import FileCache
from data.dicomfiletype import DicomFileType

MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._progressBarDialog = None
        self._initUi()

    def _initUi(self) -> None:
        # UI contains three buttons to load files, filesets and multi-filesets
        importDicomFileButton = QPushButton('Import DICOM Image...')
        importDicomFileSetButton = QPushButton('Import DICOM Image Series..')
        importDicomMultiFileSetButton = QPushButton('Import Multiple DICOM Image Series..')
        printFileCacheButton = QPushButton('Print File Cache')        
        importDicomFileButton.clicked.connect(self._importDicomFile)
        importDicomFileSetButton.clicked.connect(self._importDicomFileSet)
        importDicomMultiFileSetButton.clicked.connect(self._importDicomMultiFileSet)
        printFileCacheButton.clicked.connect(self._printFileCache)
        layout = QVBoxLayout()
        layout.addWidget(importDicomFileButton)
        layout.addWidget(importDicomFileSetButton)
        layout.addWidget(importDicomMultiFileSetButton)
        layout.addWidget(printFileCacheButton)
        widget = QWidget()
        widget.setLayout(layout)
        # Setup progress bar
        self._progressBarDialog = QProgressDialog('Importing Files...', 'Abort Import', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()
        # Setup main window
        self.setCentralWidget(widget)
        self.setWindowTitle('RapidExplorer')
        self._centerWindow()

    def _importDicomFile(self):
        # Register file
        registrar = FileRegistrar(path=FILEPATH)
        registeredMultiFileSetModel = registrar.execute()
        printer = RegisteredModelPrinter()
        printer.printMultiFileSet(registeredMultiFileSetModel)
        # cache = FileCache()
        # cache.addMultiFileSet(registeredMultiFileSetModel)

    def _importDicomFileSet(self):
        registrar = FileSetRegistrar(path=FILESETPATH, fileType=DicomFileType())        
        registeredMultiFileSetModel = registrar.execute()
        printer = RegisteredModelPrinter()
        printer.printMultiFileSet(registeredMultiFileSetModel)
        # cache = FileCache()
        # cache.addMultiFileSet(registeredMultiFileSetModel)

    def _importDicomMultiFileSet(self):
        registrar = MultiFileSetRegistrar(path=MULTIFILESETPATH, fileType=DicomFileType())
        registeredMultiFileSetModel = registrar.execute()
        printer = RegisteredModelPrinter()
        printer.printMultiFileSet(registeredMultiFileSetModel)
        # cache = FileCache()
        # cache.addMultiFileSet(registeredMultiFileSetModel)

    def _printFileCache(self):
        FileCache().printFiles()

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))