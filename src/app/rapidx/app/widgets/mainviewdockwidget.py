from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from rapidx.app.widgets.dockwidget import DockWidget
from rapidx.plugins.views.dicomfilesetview.dicomfilesetviewplugin import DicomFileSetViewPlugin


class MainViewDockWidget(DockWidget):
    def __init__(self, title: str, parent=None) -> None:
        super(MainViewDockWidget, self).__init__(title, parent=parent)
        self._viewPlugin = None
        self._initUi()

    def _initUi(self) -> None:
        self._viewPlugin = DicomFileSetViewPlugin()
        layout = QVBoxLayout()
        layout.addWidget(self._viewPlugin)
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)
