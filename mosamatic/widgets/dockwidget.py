import uuid

from PySide6.QtWidgets import QDockWidget

MENU_HEIGHT = 50


class DockWidget(QDockWidget):
    def __init__(self, title: str, parent=None) -> None:
        super(DockWidget, self).__init__(title, parent=parent)
        self.topLevelChanged.connect(self.toggleMaximize)
        self.setObjectName(str(uuid.uuid4()))

    def toggleMaximize(self):
        if self.isFloating():
            self.resize(self.parent().size())
            self.centerWindow()
        else:
            self.setFloating(False)

    def centerWindow(self):
        parentGeometry = self.parent().frameGeometry()
        geometry = self.frameGeometry()
        x = parentGeometry.x() + (parentGeometry.width() - geometry.width()) / 2
        y = parentGeometry.y() + (parentGeometry.height() - geometry.height()) / 2 + MENU_HEIGHT
        self.move(x, y)