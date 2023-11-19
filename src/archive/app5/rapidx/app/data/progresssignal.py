from PySide6.QtCore import Signal, QObject


class ProgressSignal(QObject):
    progress = Signal(int)
    finished = Signal(bool)
