from rapidx.tests.data.file.filemodel import FileModel
from rapidx.tests.data.fileset.filesetmodel import FileSetModel


class FileModelFactory:
    @staticmethod
    def create(fileSetModel: FileSetModel, path: str) -> FileModel:
        return FileModel(_path=path, _fileSetModel=fileSetModel)