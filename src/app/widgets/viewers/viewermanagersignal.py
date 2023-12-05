from PySide6.QtCore import QObject, Signal

from widgets.viewers.viewer import Viewer
from settings.settings import Settings


class ViewerManagerSignal(QObject):
    currentViewerChanged = Signal(Viewer)
    currentViewerSettingsChanged = Signal(str, Settings)