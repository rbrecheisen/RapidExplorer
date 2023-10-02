import os
import pydicom

from PySide6.QtWidgets import QFileDialog, QWidget


class DicomSeriesLoader:

    def __init__(self, parent: QWidget) -> None:
        self._parent = parent
        self.dicomSeries = []

    def execute(self) -> None:
        directory = QFileDialog.getExistingDirectory(self._parent, "Select DICOM Series")
        if not directory:
            return
        self.dicomSeries = [pydicom.dcmread(os.path.join(directory, f)) for f in os.listdir(directory)]
        for p in self.dicomSeries:
            p.decompress('pylibjpeg')
        self.dicomSeries.sort(key=lambda x: int(x.InstanceNumber))
        return self.dicomSeries