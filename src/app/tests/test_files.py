import os

from data.datamanager import DataManager

FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')


def test_dataManagerCanImportFile():
    dataManager = DataManager()
    file = dataManager.loadFile(filePath=FILEPATH)
    assert file
    assert file.id()
    assert file.path()
    assert file.name()


def test_dataManagerCanImportFileSet():
    dataManager = DataManager()
    fileSet = dataManager.loadFileSet(fileSetPath=FILESETPATH)
    assert fileSet
    print(fileSet.name())
    assert fileSet.name().startswith('fileset')


def test_cannotAddFilesIfFileSetIsLocked():
    dataManager = DataManager()
    fileSet = dataManager.loadFileSet(fileSetPath=FILESETPATH)
    assert fileSet.locked()
    try:
        fileSet.addFile('Something to trigger error')
        assert False
    except Exception:
        pass


# def test_dataManagerCanUpdateFileSetName():
#     dataManager = DataManager()
#     fileSet = dataManager.loadFileSet(fileSetPath=FILESETPATH)
#     dataManager.updateFileSetName(fileSet.id(), 'someName')


def test_dataManagerCanCreateFileSetFromFiles():
    """ This could happen when a task generates new files like the MuscleFatSegmentator.
    In that case you should save each file as a file model in the database. The file
    model should refer to an output fileset model.

    Big question:
    Do I need a FileSetModel or not? Can I just work with filesets using FileModel
    objects? Or is there some persistent aspect of filesets that I want to preserve
    over time? The fileset name is one property I might want to persist. Perhaps there
    are others? Or do I want to keep track of filesets after I restart my application?
    I think I do... 
    """
    pass