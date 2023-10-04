class Dataset:
    def __init__(self, path: str, name: str) -> None:
        self.path = path
        self.name = name
        self.fileSets = []
        
    def __str__(self) -> str:
        s = f'Dataset({self.name}):\n'
        for fileSet in self.fileSets:
            s += str(fileSet) + '\n'
        return s
