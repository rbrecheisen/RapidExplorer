from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel


class FileModelFactory:
    def create(self, fileSetModel: FileSetModel, path: str) -> FileModel:
        return FileModel(_path=path, _fileSetModel=fileSetModel)
