class Dataset:
    def __init__(self, path: str) -> None:
        self.path = path
        self.fileSets = []
    def __str__(self) -> str:
        s = 'Dataset:\n'
        for fileSet in self.fileSets:
            s += str(fileSet) + '\n'
        return s
