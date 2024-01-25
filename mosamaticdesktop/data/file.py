from mosamaticdesktop.data.models.filemodel import FileModel


class File:
    def __init__(self, model: FileModel) -> None:
        self._id = model.id
        self._name = model.name
        self._path = model.path

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def path(self) -> str:
        return self._path