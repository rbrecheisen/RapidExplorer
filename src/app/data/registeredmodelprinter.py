from data.registeredfilemodel import RegisteredFileModel
from data.registeredfilesetmodel import RegisteredFileSetModel


class RegisteredModelPrinter:
    def __init__(self, detailed=False) -> None:
        self._detailed = detailed

    def printFile(self, registeredFileModel: RegisteredFileModel) -> None:
        id = registeredFileModel.id
        path = registeredFileModel.path
        print(f'   - RegisteredFileModel(id={id}, path={path})')

    def printFileSet(self, registeredFileSetModel: RegisteredFileSetModel) -> None:
        id = registeredFileSetModel.id
        name = registeredFileSetModel.name
        path = registeredFileSetModel.path
        print(f' - RegisteredFileSetModel(id={id}, name={name}, path={path})')
        print(f'Nr. files: {registeredFileSetModel.nrFiles()}')
        if self._detailed:
            for registeredFileModel in registeredFileSetModel.registeredFileModels:
                self.printFile(registeredFileModel)

    def printMultiFileSet(self, registeredMultiFileSetModel: RegisteredFileSetModel) -> None:
        id = registeredMultiFileSetModel.id
        name = registeredMultiFileSetModel.name
        path = registeredMultiFileSetModel.path
        print(f'RegisteredMultiFileSetModel(id={id}, name={name}, path={path})')
        print(f'Nr. filesets: {registeredMultiFileSetModel.nrFileSets()}')
        print(f'Nr. files: {registeredMultiFileSetModel.nrFiles()}')
        if self._detailed:
            for registeredFileSetModel in registeredMultiFileSetModel.registeredFileSetModels:
                self.printFileSet(registeredFileSetModel)