from rapidx.tests.singleton import singleton


@singleton
class FileCache:
    """ Do I store complete datasets in here? Like MultiFileSet objects? Or only individual
    files like DICOM files?
    """
    def __init__(self) -> None:
        self._data = {}