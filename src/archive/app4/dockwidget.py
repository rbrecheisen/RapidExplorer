from PySide6.QtWidgets import QDockWidget


class DockWidget(QDockWidget):
    def __init__(self, title: str, parent=None) -> None:
        super(Dockwidget, self).__init__(title, parent=parent)
        self.topLevelChanged.connect(self._toggleMaximize)

    def _toggleMaximize(self):
        if self.isFloating():
            self.resize(self.parent().size())
            self._centerWindow()
        else:
            self.setFloating(False)

    def _centerWindow(self):
        parentGeometry = self.parent().frameGeometry()
        geometry = self.frameGeometry()
        x = parentGeometry.x() + (parentGeometry.width() - geometry.width()) / 2
        y = parentGeometry.y() + (parentGeometry.height() - geometry.height()) / 2
        self.move(x, y)