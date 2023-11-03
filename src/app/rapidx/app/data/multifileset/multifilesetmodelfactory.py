from rapidx.app.utils import create_random_name
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel


class MultiFileSetModelFactory:
    def create(self, name: str=None, path: str=None) -> MultiFileSetModel:
        if not name:
            name = create_random_name(prefix='multifileset')
        return MultiFileSetModel(_name=name, _path=path)