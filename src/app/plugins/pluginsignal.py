from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget


class PluginSignal(QObject):
    pluginChanged = Signal(QWidget)