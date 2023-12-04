from PySide6.QtWidgets import QWidget


class Viewer(QWidget):
    NAME = None
    
    def __init__(self) -> None:
        super(Viewer, self).__init__()
        # self._settings = ViewerSettings(viewerName=self.NAME)
