from PySide6.QtCore import QObject, Signal

from plugins.tasks.task import Task
from plugins.viewers.viewer import Viewer


class PluginSignal(QObject):
    taskPluginChanged = Signal(Task)
    viewerPluginChanged = Signal(Viewer)