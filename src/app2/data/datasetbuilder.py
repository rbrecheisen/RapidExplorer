import os
import utils

from data.models.dataset import Dataset
from data.models.fileset import FileSet
from data.models.file import File


class DatasetBuilder:
    def __init__(self, path: str, name: str=None) -> None:
        self.path = path
        self.name = name

    def build(self):
        data = {}
        for root, dirs, files in os.walk(self.path):
            for f_name in files:
                f_path = os.path.join(root, f_name)
                if root not in data.keys():
                    data[root] = []
                data[root].append(f_path)
        if self.name is None:
            self.name = utils.create_random_name(prefix='dataset')
        dataset = Dataset(self.path, self.name)
        for fileSetPath in data.keys():
            fileSetName = os.path.split(fileSetPath)[1]                 # Use last directory name as name
            fileSet = FileSet(path=fileSetPath, name=fileSetName)
            for filePath in data[fileSetPath]:
                file = File(path=filePath)
                fileSet.files.append(file)
            dataset.fileSets.append(fileSet)
        return dataset