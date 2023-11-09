from PySide6.QtWidgets import QWidget


class Plugin(QWidget):
    def __init__(self, parent=None):
        super(Plugin, self).__init__(parent)
        self._default = False
        self._supportedMethods = ['default', 'setDefault']

    def name(self) -> str:
        raise NotImplementedError('Not implemented')
    
    def supportedMethods(self):
        return self._supportedMethods
    
    def supportsMethod(self, name) -> bool:
        return name in self._supportedMethods

    def default(self) -> bool:
        return self._default
    
    def setDefault(self, default: bool):
        self._default = default