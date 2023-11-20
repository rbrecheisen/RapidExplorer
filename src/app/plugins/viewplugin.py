from PySide6.QtWidgets import QWidget


class ViewPlugin(QWidget):
    def __init__(self, name: str=None, widget: QWidget=None):
        super(ViewPlugin, self).__init__()
        self._name = name
        self._widget = widget

    def name(self) -> str:
        return self._name
    
    def widget(self) -> QWidget:
        return self._widget
    
    def setData(self) -> None:
        raise NotImplementedError('Not implemented')
    
    def clearData(self) -> None:
        raise NotImplementedError('Not implemented')