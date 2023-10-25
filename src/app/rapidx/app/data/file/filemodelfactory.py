from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel


class FileModelFactory:
    @staticmethod
    def create(fileSetModel: FileSetModel, path: str) -> FileModel:
        return FileModel(_path=path, _fileSetModel=fileSetModel)
