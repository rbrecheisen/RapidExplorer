from rapidx.app.file import File


class TextFile(File):

    def __init__(self, path: str, data: bytearray) -> None:
        super(TextFile, self).__init__(path)
        self._data = data

    def data(self) -> bytearray:
        return self._data

    def __str__(self) -> str:
        return f'TextFile(path={self.path()})'