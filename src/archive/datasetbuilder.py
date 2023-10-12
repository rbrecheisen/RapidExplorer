import os
import utilities

from models.dataset import Dataset
from models.fileset import FileSet
from models.file import File


class DatasetBuilder:
    def __init__(self, path: str, name: str=None) -> None:
        self._path = path
        self._name = name

    def build(self):
        data = {}
        for root, dirs, files in os.walk(self._path):
            for f_name in files:
                f_path = os.path.join(root, f_name)
                if root not in data.keys():
                    data[root] = []
                data[root].append(f_path)
        if self._name is None:
            self._name = utilities.create_random_name(prefix='dataset')
        dataset = Dataset(self._path, self._name)                         # Path points to dataset root directory
        for fileSetPath in data.keys():
            # fileSetName = os.path.split(fileSetPath)[1]
            fileSetName = os.path.relpath(fileSetPath, dataset.path)    # Get file set directory relative to dataset root directory
            fileSet = FileSet(path=fileSetPath, name=fileSetName)
            for filePath in data[fileSetPath]:
                file = File(path=filePath)
                fileSet.files.append(file)
            dataset.fileSets.append(fileSet)
        return dataset