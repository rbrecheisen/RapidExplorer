from PySide6.QtWidgets import QWidget

from widgets.dockwidget import DockWidget


class ViewsDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(ViewsDockWidget, self).__init__(title)
        self._initUi()

    def _initUi(self) -> None:
        self.setWidget(QWidget())