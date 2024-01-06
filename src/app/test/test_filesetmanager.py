from data.datamanager import DataManager


def test_managerCanCreateUpdateAndDeleteFileSet():
    fileSetPath = '/Users/Ralph/Desktop/downloads/dataset/scan1'
    
    # Create
    manager = DataManager()
    fileSet = manager.createFileSet(fileSetPath=fileSetPath)
    assert fileSet.nrFiles() > 0
    for file in fileSet.files():
        assert file.path().startswith(fileSetPath)
    assert fileSet.name() == 'scan1'
    assert fileSet.path() == fileSetPath

    # Get
    fileSet2 = manager.fileSet(fileSet.id())
    assert fileSet2
    assert fileSet2.id() == fileSet.id()

    # Update
    fileSet2.setName('scan2')
    fileSet3 = manager.updateFileSet(fileSet=fileSet2)
    assert fileSet3
    assert fileSet3.name() == 'scan2'

    # Delete
    manager.deleteFileSet(fileSet=fileSet3)
    fileSet4 = manager.fileSet(fileSet.id())
    assert fileSet4 is None