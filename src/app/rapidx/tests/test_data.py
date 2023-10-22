import os

from rapidx.tests.data.multifilesetmodelfactory import MultiFileSetModelFactory
from rapidx.tests.data.filesetmodelfactory import FileSetModelFactory
from rapidx.tests.data.filemodelfactory import FileModelFactory


FILEMODELNAME = 'image-00000.dcm'
FILEMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1/{FILEMODELNAME}')
FILESETMODELNAME = 'myFileSetModel'
FILESETMODELPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
MULTIFILESETMODELNAME = 'myMultiFileSetModel'
MULTIFILESETMODELPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')


def registerFileModel(session):
    # You should not be able to instantiate these objects directly because you need
    # knowledge of their internal variables. You don't want that!
    multiFileSetModel = MultiFileSetModelFactory.create(name=MULTIFILESETMODELNAME, path=MULTIFILESETMODELPATH)
    fileSetModel = FileSetModelFactory.create(name=FILESETMODELNAME, path=FILESETMODELPATH, multiFileSetModel=multiFileSetModel)
    fileModel = FileModelFactory.create(path=FILEMODELPATH, fileSetModel=fileSetModel)
    session.add(multiFileSetModel)
    session.add(fileSetModel)
    session.add(fileModel)
    session.commit()
    return multiFileSetModel


def test_renameFileSetModelAndMultiFileSetModel(session):
    # Register a File in the database and return as a MultiFileSet
    multiFileSetModel = registerFileModel(session)
    assert multiFileSetModel.id()
    assert multiFileSetModel.fileSetModels()[0].id()
    assert multiFileSetModel.fileSetModels()[0].fileModels()[0].id()
    # # Change name of registered MultiFileSet and FileSet and save back to database
    # multiFileSetModel.name = 'myNewMultiFileSetModel'
    # multiFileSetModel.fileSetModels()[0].name = 'myNewFileSetModel'
    # session.commit()
    # # Retrieve registered data under different names
    # mfs = session.get(MultiFileSetModel, multiFileSetModel.id())
    # fs = session.get(FileSetModel, multiFileSetModel.fileSetModels()[0].id())
    # f = session.get(FileModel, multiFileSetModel.fileSetModels()[0].fileModels()[0].id())
    # assert mfs.name() == 'myNewMultiFileSetModel'
    # assert fs.name() == 'myNewFileSetModel'
    # assert f


def test_loadDicomFile(session):
    """ Setup a separate file cache for keeping track of file contents. What should this file
    cache look like? Tree widget should allow clearing cache for specific MultiFileDataset, FileSet
    and File objects. Tree widget should show whether a file is loaded using a green or orange color.
    """
    # multiFileSetModel = registerFileModel(session)
    pass
