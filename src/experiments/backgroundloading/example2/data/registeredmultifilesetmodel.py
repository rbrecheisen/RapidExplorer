from data.multifilesetmodel import MultiFileSetModel


class RegisteredMultiFileSetModel:
    def __init__(self, multiFileSetModel: MultiFileSetModel) -> None:
        self.id = multiFileSetModel.id
        self.name = multiFileSetModel.name
        self.path = multiFileSetModel.path
        self.registeredFileSetModels = []