import os

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QVBoxLayout, QWidget, QMessageBox

from basemodel import BaseModel
from datasetstoragemanager import DatasetStorageManager
from dicomfileloader import DicomFileImporter
from dicomfilesetloader import DicomFileSetImporter
from dicomdatasetloader import DicomDatasetImporter

# TODO: Rename methods to refer to importers instead of loaders!

DATASET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILE_PATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')

engine = create_engine('sqlite://', echo=True)
BaseModel.metadata.create_all(engine)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dicomFileLoader = None
        self.dicomFileSetLoader = None
        self.dicomDatasetLoader = None
        layout = QVBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)
        self.button1 = QPushButton("Load DICOM Image")
        self.button2 = QPushButton("Load DICOM Image Series")
        self.button3 = QPushButton("Load Multiple DICOM Image Series")
        self.button1.clicked.connect(self.loadDicomFile)
        self.button2.clicked.connect(self.loadDicomFileSet)
        self.button3.clicked.connect(self.loadMultipleDicomDataset)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle('RAPID-X')

    def loadDicomFile(self):
        self.progressBar.setValue(0)
        self.dicomFileLoader = DicomFileImporter(path=FILE_PATH)
        self.dicomFileLoader.signal().done.connect(self.loadDicomFileFinished)
        self.dicomFileLoader.signal().progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(self.dicomFileLoader)

    def loadDicomFileSet(self):
        self.progressBar.setValue(0)
        self.dicomFileSetLoader = DicomFileSetImporter(path=FILESET_DIR)
        self.dicomFileSetLoader._signal.done.connect(self.loadDicomFileSetFinished)
        self.dicomFileSetLoader._signal.progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(self.dicomFileSetLoader)

    def loadMultipleDicomDataset(self):
        self.progressBar.setValue(0)
        self.dicomDatasetLoader = DicomDatasetImporter(path=DATASET_DIR)
        self.dicomDatasetLoader._signal.done.connect(self.loadDicomDatasetFinished)
        self.dicomDatasetLoader._signal.progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(self.dicomDatasetLoader)

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def loadDicomFileFinished(self, value):
        dataset = self.dicomFileLoader.data()
        with Session(engine) as session:
            manager = DatasetStorageManager(session)
            manager.save(dataset)
            self.showFinished()

    def loadDicomFileSetFinished(self, value):
        dataset = self.dicomFileSetLoader.data()
        with Session(engine) as session:
            manager = DatasetStorageManager(session)
            manager.save(dataset)
            self.showFinished()

    def loadDicomDatasetFinished(self, value):
        dataset = self.dicomDatasetLoader.data()
        with Session(engine) as session:
            manager = DatasetStorageManager(session)
            manager.save(dataset)
            self.showFinished()

    def showFinished(self):
        QMessageBox.information(self, '', 'Finished')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
