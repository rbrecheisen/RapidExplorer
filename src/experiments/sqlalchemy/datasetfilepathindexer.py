import os

from models.dataset import Dataset
from models.fileset import FileSet
from models.file import File


class DatasetFilePathIndexer:
    def __init__(self, path: str) -> None:
        self.path = path

    def load(self):
        data = {}
        for root, dirs, files in os.walk(self.path):
            for f_name in files:
                f_path = os.path.join(root, f_name)
                if root not in data.keys():
                    data[root] = []
                data[root].append(f_path)
        dataset = Dataset(self.path)
        for fileSetPath in data.keys():
            fileSet = FileSet(fileSetPath)
            for filePath in data[fileSetPath]:
                f = File(filePath)
                fileSet.files.append(f)
            dataset.fileSets.append(fileSet)
        return dataset