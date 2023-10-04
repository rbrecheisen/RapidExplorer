class FileSet:
    def __init__(self, path: str) -> None:
        self.path = path
        self.files = []
        
    def __str__(self) -> str:
        s = '  FileSet:\n'
        for f in self.files:
            s += str(f) + '\n'
        return s
