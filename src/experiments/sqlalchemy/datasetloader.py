import os


class Dataset:
    def __init__(self, path: str) -> None:
        self.path = path
        self.fileSets = []
    def __str__(self) -> str:
        s = ''
        for fileSet in self.fileSets:
            s += str(fileSet) + ', '
        return s


class FileSet:
    def __init__(self, path: str) -> None:
        self.path = path
        self.files = []
    def __str__(self) -> str:
        s = ''
        for f in self.files:
            s += str(f) + ', '
        return s


class File:
    def __init__(self, path: str) -> None:
        self.path = path
    def __str__(self) -> str:
        return self.path


class DatasetLoader:
    """ Do I actually load the DICOM files? Or do I only build a JSON dictionary 
    that defines the file hierarchy for this dataset and load the actual files
    at a later time? 
    """
    def __init__(self, path: str) -> None:
        self.path = path

    def execute(self):
        """ If you have a root directory that is equal to self.path then the files are 
        directly stored in the dataset directory, i.e., self.path. In that case, you
        need to create an artificial file set whose path is the same as the dataset's
        """
        # import pydicom
        data = {}
        for root, dirs, files in os.walk(self.path):
            for f_name in files:
                f_path = os.path.join(root, f_name)
                if f_name.endswith('.dcm'):
                    if root not in data.keys():
                        data[root] = []
                    data[root].append(f_path)
        # import json
        # print(json.dumps(data, indent=4))
        dataset = Dataset(self.path)
        for fileSetPath in data.keys():
            fileSet = FileSet(fileSetPath)
            for filePath in data[fileSetPath]:
                f = File(filePath)
                fileSet.files.append(f)
            dataset.fileSets.append(fileSet)
        return dataset