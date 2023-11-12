import os

from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QProgressDialog, QVBoxLayout,QPushButton)
from PySide6.QtGui import QGuiApplication

from data.filecache import FileCache
from data.dbsession import DbSession
from data.fileregistrar import FileRegistrar
from data.filesetregistrar import FileSetRegistrar
from data.multifilesetregistrar import MultiFileSetRegistrar
from data.multifilesetmodel import MultiFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader
from data.registeredmultifilesetcontentloader import RegisteredMultiFileSetContentLoader
from data.dicomfiletype import DicomFileType
from widgets.registeredmultifilesetmodeltreeview import RegisteredMultiFileSetModelTreeView

MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._progressBarDialog = None
        self._contentLoader = None
        self._treeView = None
        self._initUi()

    def _initUi(self) -> None:
        # UI contains three buttons to load files, filesets and multi-filesets
        importDicomFileButton = QPushButton('Import DICOM Image...')
        importDicomFileSetButton = QPushButton('Import DICOM Image Series..')
        importDicomMultiFileSetButton = QPushButton('Import Multiple DICOM Image Series..')
        printFileCacheButton = QPushButton('Print File Cache')        
        clearDatabaseButton = QPushButton('Clear DB')  
        importDicomFileButton.clicked.connect(self._importDicomFile)
        importDicomFileSetButton.clicked.connect(self._importDicomFileSet)
        importDicomMultiFileSetButton.clicked.connect(self._importDicomMultiFileSet)
        printFileCacheButton.clicked.connect(self._printFileCache)      
        clearDatabaseButton.clicked.connect(self._clearDataBase)
        # Create tree view 
        self._treeView = RegisteredMultiFileSetModelTreeView()        
        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(importDicomFileButton)
        layout.addWidget(importDicomFileSetButton)
        layout.addWidget(importDicomMultiFileSetButton)
        layout.addWidget(printFileCacheButton)
        layout.addWidget(clearDatabaseButton)
        layout.addWidget(self._treeView)
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
        # Load any models already registered
        self._loadModels()

    def _loadModels(self):
        modelLoader = RegisteredMultiFileSetModelLoader()
        registeredMultiFileSetModels = modelLoader.loadAll()
        for registeredMultiFileSetModel in registeredMultiFileSetModels:
            self._treeView.addRegisteredMultiFileSetModel(registeredMultiFileSetModel)

    def _importDicomFile(self):
        registrar = FileRegistrar(path=FILEPATH)
        registeredMultiFileSetModel = registrar.execute()
        # Run content loader in background
        self._progressBarDialog.show()
        self._progressBarDialog.setValue(0)
        self._contentLoader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel, fileType=DicomFileType)
        self._contentLoader.signal().progress.connect(self._contentLoaderProgress)
        QThreadPool.globalInstance().start(self._contentLoader)

    def _importDicomFileSet(self):
        registrar = FileSetRegistrar(path=FILESETPATH, fileType=DicomFileType())        
        registeredMultiFileSetModel = registrar.execute()
        self._contentLoader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel, fileType=DicomFileType)
        self._contentLoader.signal().progress.connect(self._contentLoaderProgress)
        QThreadPool.globalInstance().start(self._contentLoader)

    def _importDicomMultiFileSet(self):
        registrar = MultiFileSetRegistrar(path=MULTIFILESETPATH, fileType=DicomFileType())
        registeredMultiFileSetModel = registrar.execute()
        self._contentLoader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel, fileType=DicomFileType)
        self._contentLoader.signal().progress.connect(self._contentLoaderProgress)
        QThreadPool.globalInstance().start(self._contentLoader)

    def _contentLoaderProgress(self, progress):
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._treeView.addRegisteredMultiFileSetModel(self._contentLoader.data())

    def _printFileCache(self):
        FileCache().printFiles()

    def _clearDataBase(self):
        # TODO: Move this to a class?
        cache = FileCache()
        with DbSession() as session:
            multiFileSetModels = session.query(MultiFileSetModel).all()
            for multiFileSetModel in multiFileSetModels:
                registeredMultiFileSetModel = RegisteredMultiFileSetModel(multiFileSetModel)
                cache.removeMultiFileSet(registeredMultiFileSetModel)
                session.delete(multiFileSetModel)
            session.commit()
            self._treeView.model().clear()

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))