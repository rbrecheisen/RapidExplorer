from PySide6.QtGui import QStandardItem

from rapidx.app.data.fileset.filesetmodel import FileSetModel


class FileSetItem(QStandardItem):
    def __init__(self, fileSetModel: FileSetModel) -> None:
        super(FileSetItem, self).__init__(fileSetModel.name)
        self._fileSetModel = fileSetModel

    def fileSetModel(self) -> FileSetModel:
        return self._fileSetModel