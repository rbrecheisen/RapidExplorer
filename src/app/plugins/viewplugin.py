from PySide6.QtWidgets import QWidget


class ViewPlugin(QWidget):
    def __init__(self):
        super(ViewPlugin, self).__init__()

    def name(self) -> str:
        raise NotImplementedError('Not implemented')
    
    def setData(self, data) -> None:
        raise NotImplementedError('Not implemented')
