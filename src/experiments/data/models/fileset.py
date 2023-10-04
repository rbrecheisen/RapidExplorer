from models.file import File


class FileSet:
    def __init__(self, path: str) -> None:
        self.path = path
        self.files = []

    def firstFile(self) -> File:
        if len(self.files) > 0:
            return self.files[0]
        return None
        
    def __str__(self) -> str:
        s = '  FileSet:\n'
        for f in self.files:
            s += str(f) + '\n'
        return s
