import os
import threading

from data.engine import Engine
from data.filemodel import FileModel
from data.filesetmodel import FileSetModel
from data.multifilesetmodel import MultiFileSetModel
from data.databasesession import DatabaseSession
from data.fileregistrar import FileRegistrar
from data.filesetregistrar import FileSetRegistrar
from data.multifilesetregistrar import MultiFileSetRegistrar
from data.dicomfiletype import DicomFileType
from data.pngfiletype import PngFileType

MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')
NRTESTFILES = 1083


def test_engineIsSingleton():
    engine1 = Engine()
    assert engine1
    engine2 = Engine()
    assert engine1 == engine2
    assert engine1.get() == engine2.get()


def test_session():

    # Test singleton nature of engine and non-singleton nature session
    ds1 = DatabaseSession(Engine().get())    
    session1 = ds1.get()
    assert session1
    ds2 = DatabaseSession(Engine().get())
    session2 = ds2.get()
    assert session1 != session2
    session1.close()
    session2.close()

    # Save and delete some objects
    session = DatabaseSession(Engine().get()).get()
    try:
        multiFileSetModel = MultiFileSetModel()
        session.add(multiFileSetModel)
        fileSetModel = FileSetModel(multiFileSetModel=multiFileSetModel)
        session.add(fileSetModel)
        fileModel = FileModel(path=FILEPATH, fileSetModel=fileSetModel)
        session.add(fileModel)
        session.commit()
        assert multiFileSetModel.id
        assert fileSetModel.id
        assert fileModel.id
        multiFileSetModelId = multiFileSetModel.id
    finally:
        session.close()

    # Test SQLite3 in different threads
    def doOperationInSeparateThread(engine, multiFileSetModelId):
        try:
            session = DatabaseSession(engine).get()
            multiFileSetModel = session.get(MultiFileSetModel, multiFileSetModelId)
            assert multiFileSetModel.id
        finally:
            session.close()

    thread1 = threading.Thread(target=doOperationInSeparateThread, args=(Engine().get(), multiFileSetModelId))
    thread1.start()
    thread1.join()


def test_fileRegistrar():
    registrar = FileRegistrar(path=FILEPATH)
    registeredMultiFileSetModel = registrar.execute()
    assert registeredMultiFileSetModel.id
    assert registeredMultiFileSetModel.registeredFileSetModels[0].id
    assert registeredMultiFileSetModel.registeredFileSetModels[0].registeredFileModels[0].id
    # Test back-references as well
    assert registeredMultiFileSetModel.registeredFileSetModels[0].registeredMultiFileSetModel
    assert registeredMultiFileSetModel.registeredFileSetModels[0].registeredFileModels[0].registeredFileSetModel


def test_fileSetRegistrar():
    registrar = FileSetRegistrar(path=FILESETPATH, fileType=DicomFileType())
    registeredMultiFileSetModel = registrar.execute()
    assert registeredMultiFileSetModel.id 
    # Test with wrong file type (results in empty dataset)
    registrar = FileSetRegistrar(path=FILESETPATH, fileType=PngFileType())
    registeredMultiFileSetModel = registrar.execute()
    assert len(registeredMultiFileSetModel.registeredFileSetModels[0].registeredFileModels) == 0


def test_MultiFileSetRegistrar():
    registrar = MultiFileSetRegistrar(path=MULTIFILESETPATH, fileType=DicomFileType())
    registeredMultiFileSetModel = registrar.execute()
    assert registeredMultiFileSetModel.id
    assert registeredMultiFileSetModel.nrFiles() == NRTESTFILES
