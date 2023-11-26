from PySide6.QtWidgets import QDialog

from plugins.viewers.viewer import Viewer


class ViewerSettingsDialog(QDialog):
    def __init__(self, viewer: Viewer) -> None:
        self._viewer = viewer

    def viewer(self) -> Viewer:
        return self._viewer