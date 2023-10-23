from rapidx.tests.data.filemodel import FileModel
from rapidx.tests.data.filesetmodel import FileSetModel


class FileModelFactory:
    @staticmethod
    def create(fileSetModel: FileSetModel, path: str) -> FileModel:
        return FileModel(_path=path, _fileSetModel=fileSetModel)