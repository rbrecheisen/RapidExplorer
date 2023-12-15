from PySide6.QtCore import QObject, Signal


class ViewerSettingsDialogSignal(QObject):
    updated = Signal(bool)