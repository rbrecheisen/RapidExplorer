class File:
    def __init__(self, path: str) -> None:
        self._path = path

    def __str__(self) -> str:
        return f'    File: {self._path}'
