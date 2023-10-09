from PySide6.QtCore import Signal, QObject

class FileLoaderProgressSignal(QObject):
    progress = Signal(int)
