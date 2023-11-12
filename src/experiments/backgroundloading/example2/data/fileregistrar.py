from data.registrar import Registrar
from data.dbsession import DbSession
# from data.dataregistry import DataRegistry
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader


class FileRegistrar(Registrar):
    def __init__(self, path: str) -> None:
        super(FileRegistrar, self).__init__()
        self._path = path

    def execute(self) -> RegisteredMultiFileSetModel:
        with DbSession() as session:
            multiFileSetModel = MultiFileSetModel()
            session.add(multiFileSetModel)
            fileSetModel = FileSetModel(multiFileSetModel=multiFileSetModel)
            session.add(fileSetModel)
            fileModel = FileModel(path=self._path, fileSetModel=fileSetModel)
            session.add(fileModel)
            session.commit()

            # Build registered data objects
            modelLoader = RegisteredMultiFileSetModelLoader()
            registeredMultiFileSetModel = modelLoader.load(multiFileSetModel.id)
            return registeredMultiFileSetModel

        # registry = DataRegistry()
        # registeredMultiFileSetModel = registry.registerMultiFileSetModelForFile(self._path)
        # return registeredMultiFileSetModel
