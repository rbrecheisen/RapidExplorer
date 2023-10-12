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

DATASET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILE_PATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')

engine = create_engine('sqlite://', echo=True)
BaseModel.metadata.create_all(engine)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dicomFileImporter = None
        self.dicomFileSetImporter = None
        self.dicomDatasetImporter = None
        layout = QVBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)
        self.button1 = QPushButton("Import DICOM Image")
        self.button2 = QPushButton("Import DICOM Image Series")
        self.button3 = QPushButton("Import Multiple DICOM Image Series")
        self.button1.clicked.connect(self.importDicomFile)
        self.button2.clicked.connect(self.importDicomFileSet)
        self.button3.clicked.connect(self.importMultipleDicomDataset)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle('RAPID-X')

    def importDicomFile(self):
        self.progressBar.setValue(0)
        self.dicomFileImporter = DicomFileImporter(path=FILE_PATH)
        self.dicomFileImporter.signal().done.connect(self.importDicomFileFinished)
        self.dicomFileImporter.signal().progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(self.dicomFileImporter)

    def importDicomFileSet(self):
        self.progressBar.setValue(0)
        self.dicomFileSetImporter = DicomFileSetImporter(path=FILESET_DIR)
        self.dicomFileSetImporter._signal.done.connect(self.importDicomFileSetFinished)
        self.dicomFileSetImporter._signal.progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(self.dicomFileSetImporter)

    def importMultipleDicomDataset(self):
        self.progressBar.setValue(0)
        self.dicomDatasetImporter = DicomDatasetImporter(path=DATASET_DIR)
        self.dicomDatasetImporter._signal.done.connect(self.importDicomDatasetFinished)
        self.dicomDatasetImporter._signal.progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(self.dicomDatasetImporter)

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def importDicomFileFinished(self, value):
        dataset = self.dicomFileImporter.data()
        with Session(engine) as session:
            manager = DatasetStorageManager(session)
            manager.save(dataset)
            self.showFinished()

    def importDicomFileSetFinished(self, value):
        dataset = self.dicomFileSetImporter.data()
        with Session(engine) as session:
            manager = DatasetStorageManager(session)
            manager.save(dataset)
            self.showFinished()

    def importDicomDatasetFinished(self, value):
        dataset = self.dicomDatasetImporter.data()
        with Session(engine) as session:
            manager = DatasetStorageManager(session)
            manager.save(dataset)
            self.showFinished()

    def showFinished(self):
        QMessageBox.information(self, '', 'Import succeeded')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
