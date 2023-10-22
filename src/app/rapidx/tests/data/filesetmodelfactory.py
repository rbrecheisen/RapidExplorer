from rapidx.tests.data.filesetmodel import FileSetModel
from rapidx.tests.data.multifilesetmodel import MultiFileSetModel


class FileSetModelFactory:
    @staticmethod
    def create(name: str, path: str, multiFileSetModel: MultiFileSetModel) -> FileSetModel:
        return FileSetModel(_name=name, _path=path, _multiFileSetModel=multiFileSetModel)