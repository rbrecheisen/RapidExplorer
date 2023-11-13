from PySide6.QtCore import QObject, Signal


class ProgressSignal(QObject):
    progress = Signal(int)