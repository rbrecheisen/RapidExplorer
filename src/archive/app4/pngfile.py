from rapidx.app.file import File


class PngFile(File):

    def __init__(self, path: str, data: bytearray) -> None:
        super(PngFile, self).__init__(path)
        self._data = data

    def data(self) -> bytearray:
        return self._data

    def __str__(self) -> str:
        return f'PngFile(path={self.path()})'