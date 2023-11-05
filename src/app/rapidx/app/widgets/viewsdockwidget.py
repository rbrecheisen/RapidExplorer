from rapidx.app.widgets.dockwidget import DockWidget


class ViewsDockWidget(DockWidget):
    def __init__(self, title: str, parent=None) -> None:
        super(ViewsDockWidget, self).__init__(title, parent=parent)
        self._initUi()

    def _initUi(self) -> None:
        pass
