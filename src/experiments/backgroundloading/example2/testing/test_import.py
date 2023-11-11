import os

from data.fileregistrar import FileRegistrar
from data.filesetregistrar import FileSetRegistrar
from data.multifilesetregistrar import MultiFileSetRegistrar
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader
from data.dicomfiletype import DicomFileType

MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


def test_FileImport():
    # Register data in SQL database from file system paths
    registrar = FileRegistrar(path=FILEPATH)
    registeredMultiFileSetModel = registrar.execute()
    assert registeredMultiFileSetModel.id
    # Load registered models from SQL database
    modelLoader = RegisteredMultiFileSetModelLoader()
    registeredMultiFileSetModels = modelLoader.loadAll()
    assert len(registeredMultiFileSetModels) == 1

    # for registeredMultiFileSetModel in registeredMultiFileSetModels:
    #     # Load physical files and store in file cache
    #     loader = RegisteredMultiFileSetLoader(registeredMultiFileSetModel)
    #     loader.run()  # Will be called by thread later on