from data.multifilesetmodel import MultiFileSetModel


class RegisteredMultiFileSetModel:
    def __init__(self, multiFileSetModel: MultiFileSetModel) -> None:
        self.id = multiFileSetModel.id
        self.name = multiFileSetModel.name
        self.path = multiFileSetModel.path
        self.registeredFileSetModels = []
        self.loaded = False

    def nrFileSets(self) -> int:
        return len(self.registeredFileSetModels)

    def nrFiles(self) -> int:
        count = 0
        for registeredFileSetModel in self.registeredFileSetModels:
            count += registeredFileSetModel.nrFiles()
        return count