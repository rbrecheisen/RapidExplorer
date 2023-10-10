from PySide6.QtCore import Signal, QObject

class LoaderProgressSignal(QObject):
    progress = Signal(int)
    done = Signal(bool)
