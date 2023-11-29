from PySide6.QtCore import QObject, Signal


class DataManagerSigal(QObject):
    progress = Signal(int)
    finished = Signal(bool)