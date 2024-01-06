class FileType:
    NAME = None

    @staticmethod
    def check(filePath: str) -> bool:
        raise NotImplementedError('Not implemented')