from PySide6.QtCore import QObject, Signal

from widgets.viewers.viewer import Viewer


class ViewerManagerSignal(QObject):
    currentViewerChanged = Signal(Viewer)