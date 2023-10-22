from rapidx.tests.data.filemodel import FileModel
from rapidx.tests.data.filesetmodel import FileSetModel


class FileModelFactory:
    @staticmethod
    def create(path: str, fileSetModel: FileSetModel) -> FileModel:
        return FileModel(_path=path, _fileSetModel=fileSetModel)