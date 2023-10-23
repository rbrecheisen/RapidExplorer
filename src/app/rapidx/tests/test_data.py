import os

from rapidx.tests.data.multifilesetmodelfactory import MultiFileSetModelFactory
from rapidx.tests.data.multifilesetmodel import MultiFileSetModel
from rapidx.tests.data.filesetmodelfactory import FileSetModelFactory
from rapidx.tests.data.filesetmodel import FileSetModel
from rapidx.tests.data.filemodelfactory import FileModelFactory
from rapidx.tests.data.filemodel import FileModel
from rapidx.tests.data.dicomfile import DicomFile
from rapidx.tests.data.filecache import FileCache
from rapidx.tests.data.dicomfileimporter import DicomFileImporter


FILEMODELNAME = 'image-00000.dcm'
FILEMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1/{FILEMODELNAME}')
FILESETMODELNAME = 'myFileSetModel'
FILESETMODELPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
MULTIFILESETMODELNAME = 'myMultiFileSetModel'
MULTIFILESETMODELPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')


def registerFileModel(session):
    multiFileSetModel = MultiFileSetModelFactory.create(name=MULTIFILESETMODELNAME, path=MULTIFILESETMODELPATH)
    session.add(multiFileSetModel)
    fileSetModel = FileSetModelFactory.create(name=FILESETMODELNAME, path=FILESETMODELPATH, multiFileSetModel=multiFileSetModel)
    session.add(fileSetModel)
    fileModel = FileModelFactory.create(path=FILEMODELPATH, fileSetModel=fileSetModel)
    session.add(fileModel)
    session.commit()
    return multiFileSetModel


def test_renameFileSetModelAndMultiFileSetModel(session):

    # Register a File in the database and return as a MultiFileSet
    multiFileSetModel = registerFileModel(session)
    assert multiFileSetModel.id()
    assert multiFileSetModel.firstFileSetModel().id()
    assert multiFileSetModel.firstFileSetModel().firstFileModel().id()
    
    # Change name of registered MultiFileSet and FileSet and save back to database
    multiFileSetModel.setName('myNewMultiFileSetModel')
    multiFileSetModel.firstFileSetModel().setName('myNewFileSetModel')
    session.commit()
    
    # Retrieve registered data under different names
    mfs = session.get(MultiFileSetModel, multiFileSetModel.id())
    fs = session.get(FileSetModel, multiFileSetModel.firstFileSetModel().id())
    f = session.get(FileModel, multiFileSetModel.firstFileSetModel().firstFileModel().id())
    assert mfs.name() == 'myNewMultiFileSetModel'
    assert fs.name() == 'myNewFileSetModel'
    assert f.path() == FILEMODELPATH


def test_loadDicomFile(session):

    # When we want to load a single DICOM file, e.g., /path/to/dicomFile then we use 
    # the DicomFileImporter class. This class does two things: find the DICOM file in its
    # path and register it in the database. For this, it uses another class FileRegistrationHelper
    # that locates the file and builds a MultiFileSetModel object from it that contains a single
    # FileSetModel and FileModel
    importer = DicomFileImporter(path=FILEMODELPATH, session=session)
    importer.execute()
    dicomFile = importer.data()
    assert dicomFile.fileModel().id()

    # This loads a single DICOM file but returns a MultiFileSetModel object that contains
    # the DICOM file inside a FileSetModel object
    multiFileSetModel = registerFileModel(session)

    # The MultiFileSetModel, FileSetModel and FileModel objects not have a UUID primary key 
    # which you can use to do look ups in the FileCache
    # To physically load the DICOM file and do something useful with it, we need pydicom
    fileModel = multiFileSetModel.firstFileSetModel().firstFileModel()
    fileModelId = fileModel.id()

    # How could we make work? A DicomFile class could take a FileModel object and build 
    # a DICOM file representation from it, including its binary content
    # DO NOT CREATE DicomFile DIRECTLY BUT USE A FACTORY OR LOADER!
    # dicomFile = DicomFileLoader(fileModel).execute()
    dicomFile = DicomFile(fileModel)

    # The DicomFile object already contains binary data (like pixel data) so can be
    # stored in the file cache. Should we store the whole MultiFileSet object? If so, 
    # how do keep track of the fact that it's DICOM file? Naming the file in the file 
    # cache should be unique somehow. 
    # Perhaps store the DICOM file together with its corresponding MultiFileSet registration?
    cache = FileCache()
    cache.add(file=dicomFile)
    cache.add(file=dicomFile) # Try adding it twice

    # How do we retrieve this file for use? For example, when displaying it in the CT viewer
    # If we have the file model, we do it like this
    dicomFile = cache.get(fileModelId)
    cache.remove(fileModelId)
    assert not cache.get(fileModelId)
    cache.add(dicomFile)
    cache.clear()
    dicomFile = cache.get(fileModelId)
    assert not dicomFile
