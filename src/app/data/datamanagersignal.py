from PySide6.QtCore import QObject, Signal

from data.fileset import FileSet


class DataManagerSigal(QObject):
    progress = Signal(int)
    finished = Signal(FileSet)