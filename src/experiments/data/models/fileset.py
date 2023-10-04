from models.file import File


class FileSet:
    def __init__(self, path: str, name: str) -> None:
        self.path = path
        self.name = name
        self.files = []

    def firstFile(self) -> File:
        if len(self.files) > 0:
            return self.files[0]
        return None
        
    def __str__(self) -> str:
        s = f'  FileSet(name={self.name}, path={self.path}):\n'
        for f in self.files:
            s += str(f) + '\n'
        return s
