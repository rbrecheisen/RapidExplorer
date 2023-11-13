from PySide6.QtWidgets import QWidget


class ViewPlugin(QWidget):
    def __init__(self, parent=None):
        super(ViewPlugin, self).__init__(parent)

    def name(self) -> str:
        raise NotImplementedError('Not implemented')