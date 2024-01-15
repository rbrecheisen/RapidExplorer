from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox


class DicomViewer(QWidget):
    def __init__(self, parent: QWidget=None) -> None:
        super(DicomViewer, self).__init__(parent)
        self.initUi()

    def initUi(self) -> None:
        pass

    def setDicomFileSet(self) -> None:
        pass

    def addOverlayInputFileSet(self) -> None:
        pass