import os

from data.filecache import FileCache
from data.fileregistrar import FileRegistrar
from data.filesetregistrar import FileSetRegistrar
from data.multifilesetregistrar import MultiFileSetRegistrar
from data.registeredmultifilesetmodelloader import RegisteredMultiFileSetModelLoader
from data.registeredmultifilesetcontentloader import RegisteredMultiFileSetContentLoader
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

    for registeredMultiFileSetModel in registeredMultiFileSetModels:
        loader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel, fileType=DicomFileType)
        loader.run()

    cache = FileCache()
    assert cache.nrFiles() == 1