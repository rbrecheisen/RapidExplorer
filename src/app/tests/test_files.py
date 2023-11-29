import os

from data.datamanager import DataManager

FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')


def test_dataManagerCanCreateFileSetFromFilePath():
    dataManager = DataManager()
    fileSet = dataManager.importFile(filePath=FILEPATH)
    assert fileSet
    assert fileSet.id()
    assert fileSet.path()
    assert fileSet.name()
    assert fileSet.nrFiles() == 1
    assert fileSet.files()[0].name() == 'image-00000.dcm'


def test_dataManagerCanCreateFileSetFromFileSetPath():
    dataManager = DataManager()
    fileSet = dataManager.importFileSet(fileSetPath=FILESETPATH)
    assert fileSet
    assert fileSet.id()
    assert fileSet.path() == FILESETPATH
    assert fileSet.name().startswith('fileset')
    assert fileSet.nrFiles() == 361
    for file in fileSet.files():
        assert file
        assert file.id()
        assert file.name().startswith('image')


def test_dataManagerCanUpdateFileSet():
    dataManager = DataManager()
    fileSet = dataManager.importFileSet(fileSetPath=FILESETPATH)
    newName = 'someNewName'
    fileSet.setName(newName)
    newFileSet = dataManager.updateFileSet(fileSet=fileSet)
    assert newFileSet.name() == newName