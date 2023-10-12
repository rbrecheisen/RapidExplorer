import os

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QVBoxLayout, QWidget, QMessageBox

from models.basemodel import BaseModel
from datasetstoragemanager import DatasetStorageManager
from loaders.dicomfileloader import DicomFileLoader
from loaders.dicomfilesetloader import DicomFileSetLoader
from loaders.dicomdatasetloader import DicomDatasetLoader


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
        self.dicomFileLoader = DicomFileLoader(path=FILE_PATH)
        self.dicomFileLoader.signal().done.connect(self.loadDicomFileFinished)
        self.dicomFileLoader.signal().progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(self.dicomFileLoader)

    def loadDicomFileSet(self):
        self.progressBar.setValue(0)
        loader = DicomFileSetLoader(path=FILESET_DIR)
        loader._signal.done.connect(self.loadDicomFileSetFinished)
        loader._signal.progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(loader)

    def loadMultipleDicomDataset(self):
        self.progressBar.setValue(0)
        loader = DicomDatasetLoader(path=DATASET_DIR)
        loader._signal.done.connect(self.loadDicomDatasetFinished)
        loader._signal.progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(loader)

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def loadDicomFileFinished(self, value):
        dataset = self.dicomFileLoader.data()
        with Session(engine) as session:
            manager = DatasetStorageManager(session)
            manager.save(dataset)
            self.showFinished()

    def loadDicomFileSetFinished(self, value):
        pass

    def loadDicomDatasetFinished(self, value):
        pass

    def showFinished(self):
        QMessageBox.information(self, '', 'Finished')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
