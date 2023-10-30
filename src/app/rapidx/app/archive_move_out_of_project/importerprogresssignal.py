from PySide6.QtCore import Signal, QObject


class ImporterProgressSignal(QObject):
    progress = Signal(int)
    done = Signal(bool)
