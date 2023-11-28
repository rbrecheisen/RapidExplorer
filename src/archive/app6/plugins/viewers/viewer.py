from PySide6.QtWidgets import QWidget


class Viewer(QWidget):
    def __init__(self, name: str) -> None:
        super(Viewer, self).__init__()
        self._name = name

    def name(self) -> str:
        return self._name
    
    def setData(self, data) -> None:
        raise NotImplementedError('Not implemented')
    
    def clearData(self) -> None:
        raise NotImplementedError('Not implemented')