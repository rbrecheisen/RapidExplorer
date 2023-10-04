import os
import utilities

from models.dataset import Dataset
from models.fileset import FileSet
from models.file import File


class DatasetFilePathBuilder:
    def __init__(self, path: str, name: str=None) -> None:
        self.path = path
        self.name = name

    def execute(self):
        data = {}
        for root, dirs, files in os.walk(self.path):
            for f_name in files:
                f_path = os.path.join(root, f_name)
                if root not in data.keys():
                    data[root] = []
                data[root].append(f_path)
        if self.name is None:
            self.name = utilities.create_random_name(prefix='dataset')
        dataset = Dataset(self.path, self.name)
        for fileSetPath in data.keys():
            fileSet = FileSet(fileSetPath)
            for filePath in data[fileSetPath]:
                f = File(filePath)
                fileSet.files.append(f)
            dataset.fileSets.append(fileSet)
        return dataset