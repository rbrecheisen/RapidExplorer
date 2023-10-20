from rapidx.app.fileset import FileSet


class DicomFileSet(FileSet):
    def __init__(self, name: str=None, path: str=None) -> None:
        super(DicomFileSet, self).__init__(name, path)

    def sortByInstanceNumber(self) -> None:
        self.files().sort(key=lambda p: int(p.data().InstanceNumber))

    def __str__(self) -> str:
        return f'DicomFileSet(name={self.name()}, path={self.path()}, nrFiles={self.nrFiles()})'