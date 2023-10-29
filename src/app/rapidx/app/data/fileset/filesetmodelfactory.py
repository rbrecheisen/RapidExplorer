from rapidx.app.utils import create_random_name
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel


class FileSetModelFactory:
    @staticmethod
    def create(multiFileSetModel: MultiFileSetModel, name: str=None, path: str=None) -> FileSetModel:
        if not name:
            name = create_random_name(prefix='fileset')
        return FileSetModel(_name=name, _path=path, _multiFileSetModel=multiFileSetModel)
