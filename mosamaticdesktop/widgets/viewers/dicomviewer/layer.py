from PySide6.QtWidgets import QGraphicsItemGroup

from mosamaticdesktop.data.file import File


class Layer:
    def __init__(self, name: str, index: int=-1, opacity: float=0.5, visible: bool=True) -> None:
        self._name = name
        self._index = index
        self._opacity = opacity
        self._visible = visible
        self._file = None

    def name(self) -> str:
        return self._name
    
    def index(self) -> int:
        return self._index
    
    def setIndex(self, index: int) -> None:
        self._index = index

    def opacity(self) -> float:
        return self._opacity
    
    def setOpacity(self, opacity) -> None:
        self._opacity = opacity

    def visible(self) -> bool:
        return self._visible
    
    def setVisible(self, visible) -> None:
        self._visible = visible

    def file(self) -> File:
        return self._file

    def setFile(self, file: File) -> None:
        self._file = file

    def createGraphicsItem(self) -> QGraphicsItemGroup:
        raise NotImplementedError('Not implemented')