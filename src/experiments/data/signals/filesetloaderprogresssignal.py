from PySide6.QtCore import Signal, QObject

class FileSetLoaderProgressSignal(QObject):
    progress = Signal(int)